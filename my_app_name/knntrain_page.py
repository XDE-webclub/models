import reflex as rx


def knntrain():
    return rx.html('''<html><head>
    <!-- Load the latest version of TensorFlow.js -->
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/mobilenet"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/knn-classifier"></script>
</head>

<body>
    <div style="margin: 0 auto; text-align: center;">
        <div id="console"></div>
        <!-- Add an image that we will use to test -->
        <video style="margin: 0 auto; text-align: center;" autoplay="" playsinline="" muted="" id="webcam" width="224" height="224"></video>
        <br>
        <button id="class-a">Add A</button>
        <button id="class-b">Add B</button>
        <button id="class-c">Add C</button>

        <!-- Load index.js after the content of the page -->
        <p>一个实时的调用摄像头的KNN分类器</p>
        <p>请在联网环境下用先进的浏览器打开</p>
        <p>1.等待模型加载（加载完成后会提示使用摄像头）</p>
        <p>2.点击Add A则获取当前摄像头截图加入A训练集</p>
        <p>3.以此类推</p>
        <p>4.观察屏幕输出的预测结果</p>
        <p>底层由tensorflow编写</p>
    </div>
    <script>
        const classifier = knnClassifier.create();
        const webcamElement = document.getElementById('webcam');

        async function app() {
            console.log('Loading mobilenet..');

            // Load the model.
            net = await mobilenet.load();
            console.log('Successfully loaded model');

            // Create an object from Tensorflow.js data API which could capture image
            // from the web camera as Tensor.
            const webcam = await tf.data.webcam(webcamElement);

            // Reads an image from the webcam and associates it with a specific class
            // index.
            const addExample = async classId => {
                // Capture an image from the web camera.
                const img = await webcam.capture();

                // Get the intermediate activation of MobileNet 'conv_preds' and pass that
                // to the KNN classifier.
                const activation = net.infer(img, true);

                // Pass the intermediate activation to the classifier.
                classifier.addExample(activation, classId);

                // Dispose the tensor to release the memory.
                img.dispose();
            };

            // When clicking a button, add an example for that class.
            document.getElementById('class-a').addEventListener('click', () => addExample(0));
            document.getElementById('class-b').addEventListener('click', () => addExample(1));
            document.getElementById('class-c').addEventListener('click', () => addExample(2));

            while (true) {
                if (classifier.getNumClasses() > 0) {
                    const img = await webcam.capture();

                    // Get the activation from mobilenet from the webcam.
                    const activation = net.infer(img, 'conv_preds');
                    // Get the most likely class and confidence from the classifier module.
                    const result = await classifier.predictClass(activation);

                    const classes = ['A', 'B', 'C'];
                    document.getElementById('console').innerText = `
    prediction: ${classes[result.label]}\n
    probability: ${result.confidences[result.label]}
    `;

                    // Dispose the tensor to release the memory.
                    img.dispose();
                }

                await tf.nextFrame();
            }
        }

        app();
    </script>


</body></html>

''')
