// src/components/EntradaTexto.tsx
import React, { useState } from 'react';

interface EntradaTextoProps {
    onEnviar: (mensagem: string) => void;
}

const EntradaTexto: React.FC<EntradaTextoProps> = ({ onEnviar }) => {
    const [mensagem, setMensagem] = useState('');

    const handleEnviar = () => {
        if (mensagem.trim()) {
            onEnviar(mensagem);
            setMensagem('');
        }
    };

    const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
        if(event.key === 'Enter'){
            event.preventDefault();
            handleEnviar();
        }
    };

    return (
        <div className="entrada-texto">
            <input
                type="text"
                value={mensagem}
                onChange={(e) => setMensagem(e.target.value)}
                onKeyDown={handleKeyDown}//chama a função para aceitar a tecla 'Enter'
                placeholder="Digite sua mensagem..."
            />
            <button onClick={handleEnviar}>Enviar</button>
        </div>
    );
};

export default EntradaTexto;