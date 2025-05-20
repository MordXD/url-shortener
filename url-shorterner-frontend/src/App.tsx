import { useState } from 'react';

function App() {
  const [url, setUrl] = useState('');
  const [shortenedUrl, setShortenedUrl] = useState(''); // Для отображения сокращенного URL
  const [error, setError] = useState(''); // Для отображения ошибок

  // Функция для определения, является ли URL абсолютным
  const isAbsoluteUrl = (url: string) => {
    return /^(?:[a-z+]+:)?\/\//i.test(url);
  };

  const handleSubmit = async () => {
    setError('');
    setShortenedUrl('');
    if (!url) {
      setError('Пожалуйста, введите URL.');
      return;
    }

    // Проверим, что URL содержит схему (http/https)
    const processedUrl = isAbsoluteUrl(url) ? url : `http://${url}`;

    try {
      const response = await fetch('/api/shorten', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ original_url: processedUrl }),
      });

      if (!response.ok) {
        // Попытаемся прочитать тело ошибки, если оно есть
        let errorMessage = `Ошибка: ${response.status}`;
        try {
            const errorData = await response.json();
            errorMessage = errorData.detail || errorMessage;
        } catch (e) {
            // Если тело ошибки не JSON или пустое, используем статус код
        }
        throw new Error(errorMessage);
      }

      const data = await response.json();
      
      // Формируем полный URL на основе текущего хоста
      const baseUrl = window.location.origin;
      const fullShortUrl = `${baseUrl}/api/${data.short_url.split('/').pop()}`;
      
      setShortenedUrl(fullShortUrl);
    } catch (err: any) {
      setError(err.message || 'Не удалось сократить URL. Пожалуйста, попробуйте снова.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col justify-center items-center p-4 selection:bg-gray-800 selection:text-white font-sans">
      <header className="w-full max-w-3xl flex justify-center items-center py-6 absolute top-0">
        <div className="text-2xl font-medium text-gray-700" style={{ fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif' }}>Url Shorten</div>
      </header>

      <div className="w-full max-w-3xl flex flex-col items-center">
        <h1 className="text-3xl sm:text-4xl font-bold text-gray-800 mb-8 text-center" style={{ fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif' }}>
          Что мы будем сокращать дальше?
        </h1>
        <main className="bg-white p-6 sm:p-8 rounded-xl shadow-xl w-full">
          <div className="flex flex-col sm:flex-row sm:space-x-3 justify-center">
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Вставьте URL для сокращения"
              className="flex-grow p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-transparent outline-none mb-3 sm:mb-0"
              style={{ fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif' }}
            />
            <button
              onClick={handleSubmit}
              className="bg-gray-800 text-white font-bold py-3 px-6 rounded-lg hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-800 whitespace-nowrap"
              style={{ fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif' }}
            >
              Сократить
            </button>
          </div>

          {error && (
            <div className="mt-6 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg relative" role="alert">
              <strong className="font-bold">Ошибка!</strong>
              <span className="block sm:inline"> {error}</span>
            </div>
          )}

          {shortenedUrl && (
            <div className="mt-6 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded-lg relative" role="alert">
              <strong className="font-bold">Успех!</strong>
              <span className="block sm:inline"> Ваш сокращенный URL: </span>
              <a href={shortenedUrl} target="_blank" rel="noopener noreferrer" className="font-medium text-blue-600 hover:text-blue-800">
                {shortenedUrl}
              </a>
            </div>
          )}
        </main>
      </div>
      <footer className="w-full max-w-3xl flex justify-center py-6 text-center text-gray-500 text-sm absolute bottom-0">
        {/* Можно добавить информацию о копирайте или другие ссылки */}
      </footer>
    </div>
  );
}

export default App;
