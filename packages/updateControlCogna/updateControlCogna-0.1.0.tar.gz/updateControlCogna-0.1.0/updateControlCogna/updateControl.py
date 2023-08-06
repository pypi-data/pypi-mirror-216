import pandas as pd
import time 

from datetime import datetime, timedelta

class UpdateControl:
    def configInicio():
        inicioRotina    = datetime.now()

        return inicioRotina

    def configFinalSucesso(inicioRotina, nomeRelatorio, nomeRotina, diretorio):
        finalRotina     = datetime.now()
        tempoExecucao   = finalRotina - inicioRotina

        txtInicio       = inicioRotina.strftime("%d/%m/%Y %H:%M:%S")
        txtFinal        = finalRotina.strftime("%d/%m/%Y %H:%M:%S")
        txtTempo        = tempoExecucao.total_seconds()

        saidaControle   = pd.DataFrame([[txtInicio, txtFinal, nomeRelatorio, nomeRotina, txtTempo, 'Sucesso']], columns=['InicioRotina', 'FinalRotina', 'Relatorio', 'Rotina', 'TempoExecucao', 'Status'])

        try:
            atualizacoes = pd.read_csv(diretorio + '\\' + nomeRelatorio + '_' + nomeRotina + '.csv', encoding='utf-8', sep=',')
            atualizacoes = pd.DataFrame(atualizacoes, columns=['InicioRotina', 'FinalRotina', 'Relatorio', 'Rotina', 'TempoExecucao', 'Status'])

            finalArchive = atualizacoes.append(saidaControle)
            finalArchive.to_csv(diretorio + '\\' + nomeRelatorio + '_' + nomeRotina + '.csv', encoding='utf-8', sep=',')
        except:
            saidaControle.to_csv(diretorio + '\\' + nomeRelatorio + '_' + nomeRotina + '.csv', encoding='utf-8', sep=',')

    def configFinalFalha(inicioRotina, nomeRelatorio, nomeRotina, diretorio):
        finalRotina     = datetime.now()
        tempoExecucao   = finalRotina - inicioRotina

        txtInicio       = inicioRotina.strftime("%d/%m/%Y %H:%M:%S")
        txtFinal        = finalRotina.strftime("%d/%m/%Y %H:%M:%S")
        txtTempo        = tempoExecucao.total_seconds()

        saidaControle   = pd.DataFrame([[txtInicio, txtFinal, nomeRelatorio, nomeRotina, txtTempo, 'Falha']], columns=['InicioRotina', 'FinalRotina', 'Relatorio', 'Rotina', 'TempoExecucao', 'Status'])

        try:
            atualizacoes = pd.read_csv(diretorio + '\\' + nomeRelatorio + '_' + nomeRotina + '.csv', encoding='utf-8', sep=',')
            atualizacoes = pd.DataFrame(atualizacoes, columns=['InicioRotina', 'FinalRotina', 'Relatorio', 'Rotina', 'TempoExecucao', 'Status'])

            finalArchive = atualizacoes.append(saidaControle)
            finalArchive.to_csv(diretorio + '\\' + nomeRelatorio + '_' + nomeRotina + '.csv', encoding='utf-8', sep=',')
        except:
            saidaControle.to_csv(diretorio + '\\' + nomeRelatorio + '_' + nomeRotina + '.csv', encoding='utf-8', sep=',')