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

        protected override async Task OnReceived(IRequest request, string connectionId, string data)
        {
            //reenvia a mensagem para todos os clientes menos para o que enviou
            await Connection.Broadcast(connectionId+":"+data,connectionId);
            await base.OnReceived(request, connectionId, data);
        }
    }
}