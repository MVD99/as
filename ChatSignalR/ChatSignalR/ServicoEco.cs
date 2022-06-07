using Microsoft.AspNet.SignalR;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Threading.Tasks;
using System.Threading;
using System.Diagnostics;

namespace ChatSignalR
{
    public class ServicoEco : PersistentConnection
    {
        private static Int32 _totalLigacoes = 0;

        protected override Task OnConnected(IRequest request, string connectionId)
        {
            Interlocked.Increment(ref _totalLigacoes);
            Debug.WriteLine("Ligacoes: " + _totalLigacoes);
            
            return Connection.Broadcast(string.Format("{0} conectou-se ao serviço eco." + " estão " + ServicoEco._totalLigacoes + " pessoas neste chat", connectionId))
                .ContinueWith(_ => Connection.Send(connectionId, "Ola, " + connectionId + " tem "+ServicoEco._totalLigacoes+ " pessoas neste chat"));
        }

        protected override Task OnDisconnected(IRequest request, string connectionId, bool stopCalled)
        {
            Interlocked.Decrement(ref _totalLigacoes);
            Debug.WriteLine("Ligacoes: " + _totalLigacoes);

            return Connection.Broadcast(string.Format("{0} desconectou-se do serviço eco.", connectionId));
        }

        protected override Task OnReceived(IRequest request, string connectionId, string data)
        {
            //verifica se é um comando para adicionar ou remover
            var temp = data.Split(new[] { " " }, StringSplitOptions.RemoveEmptyEntries);
            //adicionar ao grupo
            if (temp.Length == 2 && temp[0].ToLower() == "adicionar")
            {
                Connection.Broadcast(connectionId + " adicionado ao chatroom de " + temp[1], connectionId);
                return this.Groups.Add(connectionId, temp[1]);
            }
            //remover do grupo
            if (temp.Length == 2 && temp[0].ToLower() == "remove")
            {
                Connection.Broadcast(connectionId + " removido do chatroom de " + temp[1], connectionId);
                return this.Groups.Remove(connectionId, temp[1]);
            }
            //mensagem de um grupo
            int i;
            i = data.IndexOf(":");
            if (i > -1)
            {
                //reenvia a mensagem para o grupo
                var groupName = data.Substring(0, i);
                var mensagem = data.Substring(i + 1);
                this.Groups.Send(groupName,connectionId+" - " +mensagem);
            }
            else
            { 
                //reenvia a mensagem para todos os clientes menos para o que enviou
                Connection.Broadcast(connectionId + " - " + data, connectionId);
            }
            return base.OnReceived(request, connectionId, data);
        }
    }
}