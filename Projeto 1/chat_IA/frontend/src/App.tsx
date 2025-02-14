// src/App.tsx
import React, { useState } from 'react';
import MenuLateral from './components/MenuLateral';
import Chat from './components/Chat';
import EntradaTexto from './components/EntradaTexto';
import './App.css';

const App: React.FC = () => {
    const [chats, setChats] = useState<{ id: number; nome: string }[]>([
        { id: 1, nome: 'CHAT 1' },
        { id: 2, nome: 'CHAT 2' },
        { id: 3, nome: 'CHAT 3' },
    ]);
    const [chatAtual, setChatAtual] = useState<number | null>(null);
    const [mensagens, setMensagens] = useState<{ id: number; texto: string; remetente: 'usuario' | 'sistema' }[]>([]);
    const [menuVisivel, setMenuVisivel] = useState(true); // Estado para controlar a visibilidade do menu

    const handleCriarChat = () => {
        const novoChat = { id: chats.length + 1, nome: `CHAT ${chats.length + 1}` };
        setChats([...chats, novoChat]);
        setChatAtual(novoChat.id);
    };

    const handleExcluirChat = (id: number) => {
        setChats(chats.filter((chat) => chat.id !== id));
        if (chatAtual === id) {
            setChatAtual(null);
            setMensagens([]);
        }
    };

    const handleSelecionarChat = (id: number) => {
        setChatAtual(id);
        // Aqui você pode carregar as mensagens do chat selecionado
    };

    const handleEnviar = (mensagem: string) => {
        if (!chatAtual) return;

        const novaMensagemUsuario = { id: mensagens.length + 1, texto: mensagem, remetente: 'usuario' as const };
        setMensagens([...mensagens, novaMensagemUsuario]);

        // Simular resposta do sistema (substituir pela chamada ao backend)
        setTimeout(() => {
            const novaMensagemSistema = { id: mensagens.length + 2, texto: 'Resposta do sistema...', remetente: 'sistema' as const };
            setMensagens((prev) => [...prev, novaMensagemSistema]);
        }, 1000);
    };

    return (
        <div className="app">
            <MenuLateral
                visivel={menuVisivel}
                onToggleMenu={() => setMenuVisivel(!menuVisivel)}
                chats={chats}
                onCriarChat={handleCriarChat}
                onExcluirChat={handleExcluirChat}
                onSelecionarChat={handleSelecionarChat}
            />
            <div className={`conteudo-principal ${!menuVisivel ? 'menu-escondido' : ''}`}>
                {chatAtual ? (
                    <>
                        <Chat mensagens={mensagens} />
                        <EntradaTexto onEnviar={handleEnviar} />
                    </>
                ) : (
                    <div className="nenhum-chat-selecionado">Selecione um chat para começar.</div>
                )}
            </div>
        </div>
    );
};

export default App;