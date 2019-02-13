#coding=utf8
import matplotlib.pyplot as plt
# 载入sklearn中样本数据集，svm算法，和矩阵处理库
from sklearn import datasets, svm, metrics
# 导入datasets样本数据集中 MNIST手写字体识别数据进digits
digits = datasets.load_digits()
images_and_labels = list(zip(digits.images, digits.target))
# 导入的数据分类图像和标签两部分，即数字图像和对应的数字标签
for index, (image, label) in enumerate(images_and_labels[:4]):
    plt.subplot(2, 4, index + 1)
    plt.axis('off')
    plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    plt.title('Training: %i' % label)
# 包括标签和图像在内的一共8组训练图像
n_samples = len(digits.images)
print "n_samples",n_samples,digits.images.shape
# 获取样本数
data = digits.images.reshape((n_samples, -1))
# 将图像转换成矩阵
classifier = svm.SVC(gamma=0.001)
# 使用SVM算法
classifier.fit(data[:n_samples // 2], digits.target[:n_samples // 2])
# 分类图像
expected = digits.target[n_samples // 2:]
predicted = classifier.predict(data[n_samples // 2:])
# 计算预测值
print("Classification report for classifier %s:\n%s\n"
      % (classifier, metrics.classification_report(expected, predicted)))
# 输出分类后的结果信息
print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))
# 输出混淆矩阵（confusion_matrix）下面介绍什么是混淆矩阵
images_and_predictions = list(zip(digits.images[n_samples // 2:], predicted))
for index, (image, prediction) in enumerate(images_and_predictions[:4]):
    plt.subplot(2, 4, index + 5)
    plt.axis('off')
    plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    plt.title('Prediction: %i' % prediction)
# 包括标签和图像在内的一共8组预测图像
plt.show()
# 输出结果图像
