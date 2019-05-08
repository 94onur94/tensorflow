# tensorflow
### Google Colaboratory üzerinde tensorflow kullanımı;

#### 1) Dataset indirme; aşağıdaki komutu, colab komut sistemine kopyalarak çalıştırınız. (root dizininde olduğunuzdan emin olunuz)
``` !wget http://download.tensorflow.org/example_images/flower_photos.tgz ```

#### 2) Dataseti dizine çıkartma; indirilen .tgz dosyasını bulunduğunuz dizine çıkartınız.
``` !tar -zxf flower_photos.tgz ```

#### 3) Eğitim ve algılama için gerekli programları indirin.
``` !wget https://raw.githubusercontent.com/94onur94/tensorflow/master/retrain.py ```

``` !wget https://raw.githubusercontent.com/94onur94/tensorflow/master/label_image.py ```
	
#### 3) Dataseti eğitme; --image_dir parametresi resimlerinizin bulunduğu klasörü belirtmektedir.
``` !python3 retrain.py --how_many_training_steps=500 --output_graph=retrained_graph.pb --output_labels=retrained_labels.txt --image_dir=flower_photos ```

#### 4) Eğitilen modeli test etme; --image parametresi tek resim sorgulamak, --image_dir parametresi klasör içindeki resimleri sorgulamak için kullanılır.
``` !python3 label_image.py --graph=retrained_graph.pb --labels=retrained_labels.txt --image=s1.jpg ```

``` !python3 label_image.py --graph=retrained_graph.pb --labels=retrained_labels.txt --image_dir=photos ```


#### retrain.py programı varsayılan olarak inception modelini kullanmaktadır. Farklı model kullanarak eğitmek için;
``` !python3 retrain.py --how_many_training_steps=500 --output_graph=retrained_graph.pb --output_labels=retrained_labels.txt --image_dir=flower_photos --tfhub_module https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/2 ```

#### label_image.py programında kullanılan modele göre input_width ve input_height parametreleri belirtilmelidir. Belirtilmediği takdirde 299*299 pixel alınır.
``` !python3 label_image.py --graph=retrained_graph.pb --labels=retrained_labels.txt --input_height=224 --input_width=224 --image=s1.jpg ```
