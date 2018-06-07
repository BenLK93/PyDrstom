
SQLinsert = ""
meta_id = 580012 # prvi meta id
post_id = 1361 #prvi post ID
post_id_last = 1362 #ni vključen
pic_id = 3197 # id slike
header_image_id = 649 #header slika id




for x in range(post_id, post_id_last): #od vključno do začetnega in do zadnjega brez njega.
	string = "INSERT INTO `wpze_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES "
	string += "("+str(meta_id)+", "+str(post_id)+", '_thumbnail_id', 3197),"
	# string += "("+str(meta_id + 1)+", "+str(post_id)+", 'gallery_images', 3197),"
	# string += "("+str(meta_id + 2)+", "+str(post_id)+", 'header_image'," + "'a:1:{i:0;s:3:"+'"'+ str(header_image_id) +'"'+";}');"
	SQLinsert += string
	post_id += 1
	meta_id += 3
	# print(string)
print(SQLinsert)

SELECT * FROM `wpze_postmeta` WHERE `meta_key`='gallery_images' AND `post_id`<1520 AND `post_id`>1363 ORDER BY `meta_id` ASC
UPDATE `wpze_postmeta` SET `meta_value` = 'a:1:{i:0;s:4:"3198";}' WHERE `meta_key`='gallery_images' AND `post_id`<1520 AND `post_id`>1363