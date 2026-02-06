import { useState } from 'react';
import { useLogin } from './useLogin';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { equipmentId, isLoading, error, login } = useLogin();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        
        const response = await login({ email, password });

        if (response.success) {
            console.log('Connexion réussie:', response);
            // TODO: Rediriger vers la page principale ou mettre à jour l'état global
        } else {
            console.error('Échec de connexion:', response.message);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#0a0908] via-[#22333b] to-[#0a0908]">
            <div className="w-full max-w-md px-8">
                {/* Logo/Titre */}
                <div className="text-center mb-10">
                    <h1 className="text-6xl font-bold text-[#f2f4f3] mb-3 tracking-tight">
                        MynodeHost
                    </h1>
                    <div className="h-1.5 w-40 bg-gradient-to-r from-[#a9927d] to-[#5e503f] mx-auto rounded-full shadow-lg"></div>
                    <p className="text-[#a9927d] mt-3 text-sm">Plateforme de gestion d'équipements</p>
                </div>

                {/* Formulaire */}
                <div className="bg-[#f2f4f3] rounded-2xl shadow-2xl p-8 border-2 border-[#a9927d]">
                    <h2 className="text-2xl font-semibold text-[#22333b] mb-6 text-center">
                        Connexion
                    </h2>

                    {/* Affichage des erreurs */}
                    {error && (
                        <div className="mb-4 p-3 bg-red-100 border-2 border-red-400 text-red-700 rounded-lg text-sm">
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-5">
                        {/* Email */}
                        <div>
                            <label 
                                htmlFor="email" 
                                className="block text-sm font-semibold text-[#22333b] mb-2"
                            >
                                Adresse email
                            </label>
                            <input
                                type="email"
                                id="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                                disabled={isLoading}
                                className="w-full px-4 py-3 bg-white text-[#0a0908] rounded-lg border-2 border-[#5e503f]
                                         focus:outline-none focus:ring-2 focus:ring-[#a9927d] focus:border-transparent
                                         placeholder-gray-400 transition-all shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                                placeholder="votre@email.com"
                            />
                        </div>

                        {/* Mot de passe */}
                        <div>
                            <label 
                                htmlFor="password" 
                                className="block text-sm font-semibold text-[#22333b] mb-2"
                            >
                                Mot de passe
                            </label>
                            <input
                                type="password"
                                id="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                                disabled={isLoading}
                                className="w-full px-4 py-3 bg-white text-[#0a0908] rounded-lg border-2 border-[#5e503f]
                                         focus:outline-none focus:ring-2 focus:ring-[#a9927d] focus:border-transparent
                                         placeholder-gray-400 transition-all shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                                placeholder="••••••••"
                            />
                        </div>

                        {/* Equipment ID - Non modifiable */}
                        <div>
                            <label 
                                htmlFor="equipmentId" 
                                className="block text-sm font-semibold text-[#22333b] mb-2"
                            >
                                ID Équipement
                                <span className="text-xs text-[#5e503f] ml-2">(attribué automatiquement)</span>
                            </label>
                            <input
                                type="text"
                                id="equipmentId"
                                value={equipmentId}
                                readOnly
                                className="w-full px-4 py-3 bg-[#e8e8e8] text-[#5e503f] rounded-lg border-2 border-[#a9927d]
                                         cursor-not-allowed font-mono font-semibold shadow-sm"
                                placeholder="Chargement..."
                            />
                        </div>

                        {/* Bouton Submit */}
                        <button
                            type="submit"
                            disabled={isLoading || !equipmentId}
                            className="w-full bg-gradient-to-r from-[#a9927d] to-[#5e503f] hover:from-[#5e503f] hover:to-[#a9927d] 
                                     text-[#f2f4f3] font-bold py-3.5 rounded-lg transition-all duration-300 
                                     shadow-lg hover:shadow-2xl transform hover:-translate-y-1 mt-6
                                     border-2 border-[#5e503f] disabled:opacity-50 disabled:cursor-not-allowed 
                                     disabled:transform-none"
                        >
                            {isLoading ? 'Connexion en cours...' : 'Se connecter'}
                        </button>
                    </form>
                </div>

                {/* Footer */}
                <p className="text-center text-[#a9927d] text-sm mt-6 font-medium">
                    © 2024 MynodeHost. Tous droits réservés.
                </p>
            </div>
        </div>
    );
}