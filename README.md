# Unknown Pleasures Effect

## Features
|Features|Description|
|------------------|-----------|
|CSS| [Materialize](https://materializecss.com/)|
|JS|[Vue.js](https://vuejs.org/index.html), [Webpack](https://webpack.js.org/), [Babel](http://babeljs.io/)|
|Python|[Flask](http://flask.pocoo.org/), [OpenCV](https://opencv.org/)|

## Development
```
git clone https://github.com/dn16/Unknown-Pleasures-Effect Unknown-Pleasures-Effect/
cd Unknown-Pleasures-Effect
rm -rf .git
pipenv install
cd frontend
npm install
```

## Script usage
### frontend
```bash
# development
npm run dev

#build the project in `~/dist` directory   
npm run build
```

### backend
```bash
# development
python3 main.py
# or
pipenv run start
```