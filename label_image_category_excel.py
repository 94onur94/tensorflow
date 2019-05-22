from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pathlib
import os
import argparse
import numpy as np
import tensorflow as tf
import xlwt 
  
workbook = xlwt.Workbook()  
  
sheet = workbook.add_sheet("Sheet Name")
style_red = xlwt.easyxf('font: bold 1, color red;')
style_green = xlwt.easyxf('font: bold 1, color green;')
style_blue = xlwt.easyxf('font: color blue;')
style_bold = xlwt.easyxf('font: bold 1')

def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph


def read_tensor_from_image_file(file_name,
                                input_height=299,
                                input_width=299,
                                input_mean=0,
                                input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(
        file_reader, channels=3, name="png_reader")
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(
        tf.image.decode_gif(file_reader, name="gif_reader"))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
  else:
    image_reader = tf.image.decode_jpeg(
        file_reader, channels=3, name="jpeg_reader")
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0)
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result

def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

def make_prediction():
    global count_right
    graph = load_graph(model_file)
    t = read_tensor_from_image_file(
        file_name,
        input_height=input_height,
        input_width=input_width,
        input_mean=input_mean,
        input_std=input_std)

    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name)
    output_operation = graph.get_operation_by_name(output_name)

    with tf.Session(graph=graph) as sess:
        results = sess.run(output_operation.outputs[0], {
            input_operation.outputs[0]: t
        })
    results = np.squeeze(results)
    top_k = results.argsort()[-5:][::-1]
    labels = load_labels(label_file)
    print(str(file_name)[len(image_dir + "/" + folder_name)+1:], labels[top_k[0]], results[top_k[0]])
    if labels[top_k[0]] == folder_name.lower():
      sheet.write(row, column, str(file_name)[len(image_dir + "/" + folder_name)+1:] + " %" + str(results[top_k[0]])[2:4], style_blue)
      count_right += 1
    else:
      sheet.write(row, column, str(file_name)[len(image_dir + "/" + folder_name)+1:] + " %" + str(results[top_k[0]])[2:4], style_red)
    

if __name__ == "__main__":
  file_name = ""
  image_dir = ""
  model_file = "retrained_graph.pb"
  label_file = "retrained_labels.txt"
  input_height = 299
  input_width = 299
  input_mean = 0
  input_std = 255
  input_layer = "Placeholder"
  output_layer = "final_result"
  if image_dir != "":  
    if len(os.listdir(image_dir)) == 0:
      print("Directory is empty")
    py = pathlib.Path().glob(image_dir + "/*")
    column=0
    avg=0
    for folder in sorted(py):
        folder_name = str(folder)[len(image_dir)+1:]
        sheet.write(0, column, folder_name, style_bold)
        index += 1
        print(folder_name)
        row=1
        total=0
        count_right=0
        py = pathlib.Path().glob(image_dir + "/" + folder_name + "/*")
        for file in sorted(py):
            file_name = str(file)
            #print(file_name)
            make_prediction()
            row += 1
            total += 1
        print(str(count_right) + " out of " + str(total) + " pictures were correctly estimated")
        print("Success rate " + str((count_right/total)*100)[:5])
        sheet.write(row, column, "%" + str((count_right/total)*100)[:5], style_green)
        avg += (count_right/total)*100
        column += 1
    print("Average success rate " + str(avg/column)[:5])
    sheet.write(1, column, "%" + "Total success rate " + str(avg/column)[:5], style_green)
    workbook.save("sample.xls")
  else:
      print("image_dir parameter is empty")