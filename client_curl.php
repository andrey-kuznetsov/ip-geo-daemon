<?php
	// create curl resource
	$ch = curl_init();

	// make curl_exec() return response body, not success status.
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);

	// set url
	curl_setopt($ch, CURLOPT_URL, "http://localhost:8080");


	$n = 0;
	while (TRUE) {
		$output = curl_exec($ch);
		echo $output, "\n";
		$parsed = json_decode($output, true);
		echo var_export($parsed, true) . "\n";
		echo "Responces got: " . $n++ . "\n";
	}

	// close curl resource to free up system resources
	curl_close($ch);     
?>