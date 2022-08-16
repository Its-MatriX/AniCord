# Гайд - получение токена через консоль

1. Открываем браузерную версию Discord
2. Нажимаем Ctrl+Shift+I
3. Переходим во вкладку КОНСОЛЬ
4. Вводим нижеуказанный код

```js
(webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()
```

5. Токен окажется в консоли. Осталось вставить его в Anicord (вводите без кавычек!)
