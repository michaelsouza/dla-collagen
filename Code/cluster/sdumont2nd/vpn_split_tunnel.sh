#!/bin/bash
# Wrapper de vpnc-script que força túnel dividido para o SDumont2.
#
# Lê:      variáveis de ambiente postas pelo vpnc (ou openconnect)
# Escreve: rotas e (opcionalmente) /etc/resolv.conf
# Chamado: Code/cluster/sdumont2nd/vpn_connect.sh
#
# Por que existe: o gateway do LNCC empurra rota default pelo túnel (túnel
# completo). Com isso, todo o tráfego da máquina passa a sair pelo LNCC e o que
# ele não roteia — pypi, github, DNS público — para de funcionar. Este wrapper
# descarta a rota default do servidor e injeta apenas a faixa do SDumont2 antes
# de chamar o vpnc-script real.
#
# Serve tanto ao vpnc quanto ao openconnect: os dois usam a mesma interface de
# script, com as mesmas variáveis CISCO_SPLIT_INC_*.
#
# Alargue SPLIT_NET se precisar de outros serviços do LNCC.

set -u

SPLIT_ADDR="${SDUMONT_SPLIT_ADDR:-146.134.176.0}"
SPLIT_MASK="${SDUMONT_SPLIT_MASK:-255.255.255.0}"
SPLIT_LEN="${SDUMONT_SPLIT_MASKLEN:-24}"

# Substitui o que o servidor mandou por exatamente uma rota.
export CISCO_SPLIT_INC=1
export CISCO_SPLIT_INC_0_ADDR="$SPLIT_ADDR"
export CISCO_SPLIT_INC_0_MASK="$SPLIT_MASK"
export CISCO_SPLIT_INC_0_MASKLEN="$SPLIT_LEN"

# Preserva o DNS local. O WSL está em networkingMode=mirrored com
# dnsTunneling=true: as consultas passam pelo Windows, e deixar o vpnc-script
# reescrever /etc/resolv.conf com os servidores internos do LNCC quebra a
# resolução de tudo que é externo. O SDumont resolve publicamente, então não
# precisamos do DNS interno.
if [ "${SDUMONT_KEEP_DNS:-1}" = "1" ]; then
    unset INTERNAL_IP4_DNS
    unset INTERNAL_IP6_DNS
    unset CISCO_DEF_DOMAIN
fi

exec /usr/share/vpnc-scripts/vpnc-script "$@"
