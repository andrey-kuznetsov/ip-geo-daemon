<?php
	// create curl resource
	$ch = curl_init();

	// make curl_exec() return response body, not success status.
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);

	// set url
	curl_setopt($ch, CURLOPT_URL, "http://localhost:8080");


	while (TRUE) {
		$output = curl_exec($ch);
		echo $output;
	}

	// close curl resource to free up system resources
	curl_close($ch);     
?>