// src/components/ChatItem.tsx
import React from 'react';

interface ChatItemProps {
    chat: { id: number; nome: string };
    onExcluir: () => void;
    onSelecionar: () => void;
}

const ChatItem: React.FC<ChatItemProps> = ({ chat, onExcluir, onSelecionar }) => {
    return (
        <div className="chat-item" onClick={onSelecionar}>
            <span>{chat.nome}</span>
            <button onClick={(e) => { e.stopPropagation(); onExcluir(); }} className="botao-excluir">
                X
            </button>
        </div>
    );
};

export default ChatItem;