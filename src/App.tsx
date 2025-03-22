import { useState, useEffect } from 'react';
import axios from 'axios';
import { FaGithub } from 'react-icons/fa';

interface Conspiracy {
    id: string;
    conspiracy: string;
    sources: string[];
}

export default function MandelaMachine() {
    const [conspiracy, setConspiracy] = useState<Conspiracy | null>(null);
    const [conspiracyID, setConspiracyID] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(false);

    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const conspiracyId = urlParams.get('id');
        if (conspiracyId) {
            fetchConspiracy(conspiracyId);
        } else {
            generateConspiracy();
        }
    }, []);

    const generateConspiracy = async () => {
        setLoading(true);
        try {
            const response = await axios.get<Conspiracy>(
                'https://mandela-machine.onrender.com/generate'
            );
            setConspiracy(response.data);
            setConspiracyID(response.data.id);
        } catch (error) {
            console.error('Error fetching conspiracy:', error);
        }
        setLoading(false);
    };

    const fetchConspiracy = async (id: string) => {
        setLoading(true);
        try {
            const response = await axios.get<Conspiracy>(
                `https://mandela-machine.onrender.com/conspiracy/${id}`
            );
            setConspiracy(response.data);
        } catch (error) {
            console.error('Error fetching conspiracy by ID:', error);
        }
        setLoading(false);
    };

    const copyPermalink = () => {
        if (conspiracy) {
            const permalink = `${window.location.origin}?id=${conspiracy.id}`;
            navigator.clipboard.writeText(permalink);
            window.history.pushState({}, '', `?id=${conspiracyID}`);
        }
    };

    return (
        <div className='flex h-screen flex-col items-center justify-center bg-white p-6 text-gray-900'>
            {loading ? (
                <p className='text-gray-500'>Generating conspiracy...</p>
            ) : conspiracy ? (
                <div className='w-full max-w-2xl'>
                    <p className='mb-4 font-ebgaramond text-3xl'>
                        {conspiracy.conspiracy}
                    </p>
                    <div className='mb-4'>
                        <p className='text-md font-mono text-gray-500'>
                            Sources:
                        </p>
                        <ul className='mt-2 space-y-1'>
                            {conspiracy.sources.map((source, index) => (
                                <li key={index}>
                                    <a
                                        href={source}
                                        target='_blank'
                                        rel='noopener noreferrer'
                                        className='font-mono text-blue-600 hover:text-blue-500 hover:underline'
                                    >
                                        {source}
                                    </a>
                                </li>
                            ))}
                        </ul>
                    </div>
                    <div className='flex gap-4'>
                        <button
                            onClick={copyPermalink}
                            className='text-md rounded bg-transparent px-0 py-0 font-mono text-gray-300 hover:underline'
                        >
                            [permalink]
                        </button>
                    </div>
                </div>
            ) : (
                <p className='text-red-500'>Error loading conspiracy.</p>
            )}

            <div className='absolute bottom-10 flex items-center gap-2 text-gray-600 transition hover:text-black'>
                <a
                    href='https://github.com/AdvaySanketi/mandela-machine/'
                    target='_blank'
                    rel='noopener noreferrer'
                    className='flex items-center gap-2 text-gray-600 transition hover:text-black'
                >
                    {FaGithub({ className: 'text-2xl' }) as JSX.Element}
                    <span className='font-mono text-sm'>View on GitHub</span>
                </a>
            </div>
        </div>
    );
}
