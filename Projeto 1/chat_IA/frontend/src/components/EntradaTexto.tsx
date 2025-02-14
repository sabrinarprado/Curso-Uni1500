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

    return (
        <div className="entrada-texto">
            <input
                type="text"
                value={mensagem}
                onChange={(e) => setMensagem(e.target.value)}
                placeholder="Digite sua pergunta..."
            />
            <button onClick={handleEnviar}>Enviar</button>
        </div>
    );
};

export default EntradaTexto;