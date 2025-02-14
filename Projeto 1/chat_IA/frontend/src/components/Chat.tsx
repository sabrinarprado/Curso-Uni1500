import React from "react";


interface Mensagem {
    id: number;
    texto: string;
    remetente: 'usuario' | 'sistema';
}

interface ChatProps {
    mensagens: Mensagem[];
}

const Chat: React.FC<ChatProps> = ({ mensagens}) => {
    return(
        <div className="chat">
            {mensagens.map((msg) => (
                <div key={msg.id} className={`mensagem ${msg.remetente}`}>
                    {msg.texto}
                </div>
            ))}
        </div>
    );
};
export default Chat;