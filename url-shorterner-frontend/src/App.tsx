import { useState } from 'react';
// Убедитесь, что вы установили heroicons: npm install @heroicons/react
import { LinkIcon, ClipboardDocumentIcon, CheckCircleIcon } from '@heroicons/react/24/outline';

function App() {
  const [url, setUrl] = useState('');
  const [shortenedUrl, setShortenedUrl] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const isAbsoluteUrl = (url: string) => {
    return /^(?:[a-z+]+:)?\/\//i.test(url);
  };

  const handleSubmit = async () => {
    setError('');
    setShortenedUrl('');
    setCopied(false); // Сбрасываем статус копирования при новой отправке
    if (!url) {
      setError('Пожалуйста, введите URL.');
      return;
    }

    setIsLoading(true);
    const processedUrl = isAbsoluteUrl(url) ? url : `http://${url}`;

    try {
      // Имитация API запроса для демонстрации
      await new Promise(resolve => setTimeout(resolve, 1500));
      // const response = await fetch('/api/shorten', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ original_url: processedUrl }),
      // });

      // if (!response.ok) {
      //   let errorMessage = `Ошибка: ${response.status}`;
      //   try {
      //     const errorData = await response.json();
      //     errorMessage = errorData.detail || errorMessage;
      //   } catch (e) { /* ignore */ }
      //   throw new Error(errorMessage);
      // }
      // const data = await response.json();
      
      // Имитируем ответ API для примера
      const shortCode = Math.random().toString(36).substring(2, 8);
      const baseUrl = window.location.origin;
      // На картинке URL выглядит как прямой /shortcode, а не /api/shortcode
      const fullShortUrl = `${baseUrl}/${shortCode}`; 
      
      setShortenedUrl(fullShortUrl);

    } catch (err: any) {
      setError(err.message || 'Не удалось сократить URL. Пожалуйста, попробуйте снова.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = () => {
    if (!shortenedUrl) return;
    navigator.clipboard.writeText(shortenedUrl).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2500); // Сообщение "Скопировано" исчезнет через 2.5 сек
    }).catch(err => {
      console.error('Ошибка копирования: ', err);
      setError('Не удалось скопировать ссылку в буфер обмена.');
    });
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col items-center p-4 sm:p-8 font-sans selection:bg-pink-500 selection:text-white">
      
      {/* Декоративный элемент как на картинке */}
      <div className="absolute top-5 right-5 sm:top-8 sm:right-8 w-12 h-12 sm:w-16 sm:h-16 bg-gradient-to-br from-pink-400 to-purple-500 rounded-full opacity-70 blur-sm"></div>

      <header className="w-full max-w-xl mx-auto pt-12 pb-8 sm:pt-20 sm:pb-12 text-center relative z-10">
        {/* Можно добавить логотип слева, как "Codex", если есть */}
        {/* <img src="/your-logo.svg" alt="App Logo" className="h-7 absolute top-1/2 left-0 -translate-y-1/2" /> */}
        <h1 className="text-3xl sm:text-4xl font-bold text-slate-900 font-heading">
          Что мы будем сокращать дальше?
        </h1>
      </header>

      <main className="w-full max-w-xl bg-white p-6 sm:p-8 rounded-xl sm:rounded-2xl shadow-xl relative z-10">
        <div className="space-y-6">
          {/* Поле ввода, стилизованное под элементы на картинке */}
          <div className="relative">
            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3.5">
              <LinkIcon className="h-5 w-5 text-slate-400" aria-hidden="true" />
            </div>
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com/очень-длинный-url"
              className="block w-full rounded-lg border-0 py-3.5 pl-11 pr-4 text-slate-900 bg-slate-100 ring-1 ring-inset ring-slate-200 placeholder:text-slate-400 focus:bg-white focus:ring-2 focus:ring-inset focus:ring-pink-500 sm:text-sm sm:leading-6 transition-all"
            />
          </div>

          {/* Кнопка, стилизованная под "Code" */}
          <button
            onClick={handleSubmit}
            disabled={isLoading}
            className="w-full flex items-center justify-center px-6 py-3 border border-transparent text-base font-semibold rounded-full shadow-sm text-white bg-slate-900 hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-800 disabled:opacity-60 transition-colors"
          >
            {isLoading ? (
              <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            ) : (
              'Сократить URL'
            )}
          </button>
        </div>

        {error && (
          <div className="mt-6 p-4 border-l-4 border-red-400 bg-red-50 text-red-700 rounded-md" role="alert">
            <strong className="font-bold">Ошибка! </strong>
            <span className="block sm:inline">{error}</span>
          </div>
        )}

        {shortenedUrl && (
          <div className="mt-8 pt-6 border-t border-slate-200/80">
            {/* Можно добавить заголовок "Tasks" или "Результат" */}
            {/* <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">Результат</h2> */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between p-3.5 bg-slate-50 rounded-lg ring-1 ring-slate-200/80">
              <a 
                href={shortenedUrl} 
                target="_blank" 
                rel="noopener noreferrer" 
                className="text-pink-600 hover:text-pink-700 font-medium break-all text-sm sm:text-base truncate"
                title={shortenedUrl}
              >
                {shortenedUrl}
              </a>
              <button
                onClick={handleCopy}
                title="Скопировать ссылку"
                className={`mt-3 sm:mt-0 sm:ml-4 inline-flex items-center shrink-0 px-3.5 py-1.5 border border-transparent text-xs font-medium rounded-full shadow-sm ${
                  copied 
                    ? 'bg-green-100 text-green-700 hover:bg-green-200' 
                    : 'bg-slate-200 text-slate-700 hover:bg-slate-300'
                } focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-pink-500 transition-all`}
              >
                {copied ? (
                  <CheckCircleIcon className="h-4 w-4 mr-1.5" />
                ) : (
                  <ClipboardDocumentIcon className="h-4 w-4 mr-1.5" />
                )}
                {copied ? 'Скопировано!' : 'Копировать'}
              </button>
            </div>
          </div>
        )}
      </main>

      <footer className="w-full max-w-xl mx-auto py-10 mt-auto text-center">
        <p className="text-slate-400 text-xs font-sans">
          &copy; 2024 Сокращатель URL
        </p>
      </footer>
    </div>
  );
}

export default App;