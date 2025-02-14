// src/components/MenuLateral.tsx
import React from 'react';
import ChatItem from './ChatItem';

interface MenuLateralProps {
    visivel: boolean;
    onToggleMenu: () => void;
    chats: { id: number; nome: string }[];
    onCriarChat: () => void;
    onExcluirChat: (id: number) => void;
    onSelecionarChat: (id: number) => void;
}

const MenuLateral: React.FC<MenuLateralProps> = ({ visivel, onToggleMenu, chats, onCriarChat, onExcluirChat, onSelecionarChat }) => {
    return (
        <div className={`menu-lateral ${visivel ? 'visivel' : ''}`}>
            <div className="cabecalho-menu">
                <button onClick={onCriarChat} className="botao-novo-chat">
                    + NOVO CHAT
                </button>
                <button onClick={onToggleMenu} className="botao-toggle-menu">
                    {visivel ? '◄' : '►'}
                </button>
            </div>
            <div className="lista-chats">
                {chats.map((chat) => (
                    <ChatItem
                        key={chat.id}
                        chat={chat}
                        onExcluir={() => onExcluirChat(chat.id)}
                        onSelecionar={() => onSelecionarChat(chat.id)}
                    />
                ))}
            </div>
        </div>
    );
};

export default MenuLateral;