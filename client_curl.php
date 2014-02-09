<?php
	$ch = curl_init();

	// make curl_exec() return response body, not success status.
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);



	$ips = explode("\n", '221.193.237.73
	183.63.130.218
	222.124.143.9
	221.204.223.38
	220.162.237.125
	221.215.173.78
	203.161.24.62
	91.143.57.8
	85.26.164.199
	78.36.41.96
	2.60.0.77
	188.232.98.242
	188.232.98.242
	84.38.176.247
	116.228.55.217
	217.244.61.96
	'
	);

	while (TRUE) {
		foreach($ips as $ip){
			$ip = trim($ip);
			if(empty($ip)) continue;
			echo $ip;
			curl_setopt($ch, CURLOPT_URL, "http://localhost:8081/getCityFull?ip=" . $ip);
			$output = curl_exec($ch);
			echo $output, "\n";
			$parsed = json_decode($output, true);
			echo var_export($parsed, true) . "\n";
		}
	}

	curl_close($ch);     
?>