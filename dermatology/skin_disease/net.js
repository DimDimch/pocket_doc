var tf = require('@tensorflow/tfjs');
var tfn = require('@tensorflow/tfjs-node');
const { Image } = require('image-js');

TARGET_CLASSES = {
  0: 'Актинический кератоз или болезнь Боуэна', //Actinic Keratoses (Solar Keratoses) or intraepithelial Carcinoma (Bowen’s disease), akiec
  1: 'Базально-клеточная карцинома', //'Basal Cell Carcinoma', bcc
  2: 'Доброкачественный кератоз', //'Benign Keratosis', bkl
  3: 'Дерматофиброма', //'Dermatofibroma', df
  4: 'Меланома', //'Melanoma', mel
  5: 'Меланоцитарный невус', //'Melanocytic Nevi', nv
  6: 'Сосудистое поражение кожи'//'Vascular skin lesion', vasc
};

const model_makePrediction = async(dataURL) => {

	let model;
    model = await tf.loadLayersModel('http://skin.test.woza.work/final_model_kaggle_version1/model.json');

    let image = await Image.load(dataURL);

    let tensor = tf.browser.fromPixels(image).resizeNearestNeighbor([224,224]).toFloat();
	let offset = tf.scalar(127.5);
	tensor = tensor.sub(offset).div(offset).expandDims();

	let predictions = await model.predict(tensor).data();
	let top3 = Array.from(predictions)
		.map(function (p, i) { // this is Array.map
			return {
				probability: p * 100,
				className: TARGET_CLASSES[i] // we are selecting the value from the obj
			};

		}).sort(function (a, b) {
			return b.probability - a.probability;

		}).slice(0, 3);
	console.clear();
	console.log("!!!!", top3[0].className, ",", top3[0].probability, ",", top3[1].className, ",", top3[1].probability, ",", top3[2].className, ",", top3[2].probability, ", ", '!!!!');
}

(async() => model_makePrediction(process.argv[2]))()