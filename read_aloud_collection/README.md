### Collection of different API wrappers to use with tts_reader.py

All the scripts in /scripts implement a different API to be funneled into the [Voice RSS API](http://www.voicerss.org).

Although you can run each script separately, its intended use as a group is exemplified on collection_example.py, 
where many of them are aggregated into a single call to provide some sort of daily information.

Be advised that calling all of them together takes a few minutes to process, specially the news feeds return too much text.

**Important:**
* You need to get an API key to use tts_reader.py ([Click here](http://www.voicerss.org/login.aspx)), currency_exchange_data.py ([Click here](https://free.currencyconverterapi.com/free-api-key)), and stock_price.py ([Click here](https://financialmodelingprep.com/login))
* elmundo_headlines.py and lanacion_headlines.py return in spanish. If you use this, or plan to extend with results in any other language, remember to
set your prefered voice language via the optional parameter language= in the call to read_tts_single(). 
* The possible languages for the Voice RSS API are available [here](http://www.voicerss.org/api/)

**Scripts:**
* bbc_headlines.py: Reads aloud the newest [BBC](https://www.bbc.com/news/10628494) headlines by tag.
* bored_advice.py: Reads aloud an activity to do when bored from [Bored API](https://www.boredapi.com)
* church_calendar.py: Reads aloud the Roman Catholic church celebrations for today, from [Calapi API](http://calapi.inadiutorium.cz)
* cnn_headlines.py: Reads aloud the newest [CNN](http://edition.cnn.com/services/rss/) headlines by tag.
* crypto_exchange_data.py: Reads aloud the crypto exchange price between two symbols, from [Cryptonator API](https://www.cryptonator.com/api)
* currency_exchange_data.py: Reads aloud the currency exchange price between two symbols, from [CurrencyConverter API](https://www.currencyconverterapi.com/)
| Needs an API KEY
* design_quotes.py: Reads aloud a design quote from [Quotes on Design API](http://quotesondesign.com)
* elmundo_headlines.py: Reads aloud the newest [El Mundo](http://rss.elmundo.es/rss/) headlines by tag.
* hackernews_top_stories.py: Reads aloud the titles of the top 30 [Hackernews](https://github.com/HackerNews/API) stories
* lanacion_headlines.py: Read aloud the newest [La Nacion](https://servicios.lanacion.com.ar/herramientas/rss/ayuda) headlines for latest news.
* national_holidays_calendar.py: Reads aloud national holidays for today from [Nager.date API](https://date.nager.at/)
* quotes.py: Reads aloud a quote from [Forismatic API](https://forismatic.com/en/)
* random_advice.py: Reads aloud a random advice from [Advice Slip API](https://api.adviceslip.com/)
* rt_headlines.py: Read aloud the newest [RT](https://www.rt.com/rss-feeds/) headlines by tag.
* stock_price.py: Reads aloud the updated price of a stock, from [Financial Modelling Prep API](https://financialmodelingprep.com/developer/docs) | Needs an API KEY
* weather.py: Reads aloud the weather from [MetaWeather API](https://www.metaweather.com/api/)








