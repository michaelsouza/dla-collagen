#!/bin/bash
# Sobe a VPN do LNCC em túnel dividido e confere que a rede local sobreviveu.
#
# Lê:      ~/sdumont.conf (config do vpnc; contém segredo, fora do git)
# Escreve: interface tun0, uma rota para a faixa do SDumont2
# Chamado: à mão, com sudo, antes de trabalhar no cluster
#
# Por que existe: o gateway do LNCC (146.134.0.14) empurra rota default pelo
# túnel. Com o vpnc-script padrão isso derruba o acesso a tudo que não é LNCC —
# pypi, github, DNS público. O gateway fala apenas IPsec/IKEv1 (a porta 443 está
# fechada, então openconnect não serve), então a saída é manter o vpnc e trocar
# só o script de configuração.
#
# Desconectar: sudo vpnc-disconnect

set -u

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
WRAPPER="$REPO/Code/cluster/sdumont2nd/vpn_split_tunnel.sh"
CONF="${SDUMONT_VPNC_CONF:-$HOME/sdumont.conf}"
SDUMONT_HOST="login.sdumont2nd.lncc.br"
PROVA_EXTERNA="github.com"

if [ "$(id -u)" -ne 0 ]; then
    echo "Rode com sudo: sudo -E $0" >&2
    exit 1
fi
[ -r "$CONF" ]    || { echo "config não encontrada: $CONF" >&2; exit 1; }
[ -x "$WRAPPER" ] || { echo "wrapper não encontrado: $WRAPPER" >&2; exit 1; }

if ip link show tun0 >/dev/null 2>&1; then
    echo "tun0 já existe — desconectando antes de subir de novo."
    vpnc-disconnect || true
    sleep 1
fi

echo "Conectando com túnel dividido (script: $(basename "$WRAPPER"))..."
# --local-port 0: o Windows já mantém UDP 500 e 4500 abertas (serviço de IPsec),
# e como o WSL está em networkingMode=mirrored ele compartilha essa pilha — o
# vpnc não consegue fazer bind na 500 e falha com "Address already in use".
# Com 0, o kernel escolhe uma porta de origem efêmera; o NAT-T cuida do resto.
# --enable-weak-encryption: o concentrador do LNCC só oferece 3DES, que o vpnc
# recusa por padrão. Não há escolha do nosso lado — ou aceita, ou não conecta.
# O risco é limitado porque o que trafega é SSH, que traz a própria criptografia
# moderna por dentro do túnel; o 3DES protege apenas o envelope IPsec.
# A ordem abaixo reproduz o comando que Michael já usava e que funciona
# (config primeiro, flags depois); a única adição é --script.
vpnc "$CONF" --enable-weak-encryption --local-port 0 --script "$WRAPPER" \
    || { echo "vpnc falhou" >&2; exit 1; }
sleep 2

echo
echo "=== rotas ==="
ip route | sed 's/^/  /'

falhas=0
echo
echo "=== verificação ==="

# 1. A rota default NÃO pode ter ido para o túnel. É o defeito que este script existe para evitar.
if ip route show default | grep -q tun0; then
    echo "  FALHOU  a rota default foi para o tun0 — o túnel dividido não pegou"
    falhas=$((falhas + 1))
else
    echo "  ok      rota default intacta (não passa pelo tun0)"
fi

# 2. O cluster precisa responder; é o motivo de existir a VPN.
if timeout 20 bash -c "</dev/tcp/$SDUMONT_HOST/22" 2>/dev/null; then
    echo "  ok      SSH do SDumont2 alcançável"
else
    echo "  FALHOU  SDumont2 continua inalcançável"
    falhas=$((falhas + 1))
fi

# 3. E o resto da internet precisa continuar de pé, que era o problema original.
if timeout 15 getent hosts "$PROVA_EXTERNA" >/dev/null 2>&1; then
    echo "  ok      DNS externo funciona ($PROVA_EXTERNA resolve)"
else
    echo "  FALHOU  DNS externo quebrou — o túnel sequestrou a resolução"
    falhas=$((falhas + 1))
fi

echo
if [ "$falhas" -eq 0 ]; then
    echo "VPN de pé, rede local preservada. Desconectar: sudo vpnc-disconnect"
else
    echo "$falhas verificação(ões) falharam. Para voltar ao estado anterior:"
    echo "  sudo vpnc-disconnect"
    exit 1
fi
