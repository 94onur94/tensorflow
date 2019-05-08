# tensorflow

#### 1) Dataset indirme; aşağıdaki komutu, colab komut sistemine kopyalarak çalıştırınız. (root dizininde olduğunuzdan emin olunuz)
``` !wget http://download.tensorflow.org/example_images/flower_photos.tgz ```

#### 2) Dataseti dizine çıkartma; indirilen .tgz dosyasını bulunduğunuz dizine çıkartınız.
!tar -zxf flower_photos.tgz

#### 3) Eğitim ve algılama için gerekli programları indirin
!wget https://github.com/tensorflow/hub/raw/master/examples/image_retraining/retrain.py
!wget https://github.com/tensorflow/tensorflow/raw/master/tensorflow/examples/label_image/label_image.py
	
#### 3) Dataseti eğitme; --image_dir parametresi resimlerinizin bulunduğu klasörü belirtmektedir.
!python3 retrain.py --how_many_training_steps=500 --output_graph=retrained_graph.pb --output_labels=retrained_labels.txt --image_dir=flower_photos

#### 4) Eğitilen modeli test etme; --image parametresi tek resim sorgulamak, --image_dir parametresi klasör içindeki resimleri sorgulamak için kullanılır
!python3 label_image.py --graph=retrained_graph.pb --labels=retrained_labels.txt --image=s1.jpg
!python3 label_image.py --graph=retrained_graph.pb --labels=retrained_labels.txt --image_dir=photos
