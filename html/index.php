<!DOCTYPE html>
<html>
<?php
    // if form is submitted, run python script with text as message
    if (isset($_POST['text-to-speech'])) {
        $text = $_POST['message'];
	// send argument to terminal with message
        //$runScript = exec("python3 /home/pi/PycharmProjects/raspberrypi-camera/textToSpeech.py '$text'");
    }
    if (isset($_POST['add-face'])) {
    	$name = $_POST['addFace'];
	$runScript = exec("sudo python3 /home/pi/PycharmProjects/raspberrypi-camera/encode_faces.py -n '$name'");
	$runScript;
    }
?>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=Edge">
    <title>Front Doorbell</title>
    <!-- styling import -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" >
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<body>
<div class="container-fluid">
    <h1>Front Doorbell</h1>
    <img src="http://142.222.68.4:8081/" onerror="this.src='image/camera.png'" width="640" height="480"/>
    <form method="post">
	<div class="form-group">
        	<div class="col-sm-5">
            		<label for="message">Message:</label>
            		<textarea class="form-control" rows="5" name="message"></textarea>
            		<br>
            		<button class="btn" name="text-to-speech">Send</button>
        	</div>
	</div>
	<div class="col-sm-7"></div>
	<div class="form-group">
		<div class="col-sm-5">
			<label for="addFace">Add to Database:</label>
            		<input class="form-control" placeholder="firstname_lastname" name="addFace"></textarea>
            		<br>
            		<button class="btn" name="add-face">Add</button>
		</div>
	</div>
    </form>
 </body>
</html>
