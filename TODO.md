# TODO: Corrigir horários no extrato

**Plano aprovado e implementado.**

## Passos:
- [x] 1. Criar função helper `formatar_data_local()` em extrato.py
- [x] 2. Substituir blocos duplicados de formatação de data nas seções de vendas e pagamentos pela função helper
- [x] 3. Verificar ordenação por data (já usa strings formatadas corretamente)
- [x] 4. Testar página de extrato: timestamps devem coincidir com horários de registro (sem -3h)
- [x] 5. Confirmar conclusão com attempt_completion

**Status: Completo. Horários no extrato agora exibem corretamente sem desfazimento de 3 horas.**


