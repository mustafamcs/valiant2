<?php
function ItemDetay($value,$itemDetay,$itemIcon,$efsunID,$efsunText)
{
  $html = '<table class="table table-bordered">
  <tr>
  <th>Eşya İkonu</th>
  <td class="text-center"><img src="'.base_url('assets/img/icon/'.$itemIcon).'"></td>
  </tr>';
  $html .= '<tr>
  <th>Eşya ID\'si</th>
  <td class="text-center">'.$itemDetay->id.'</td>
  </tr>';
  $html .= '<tr>
  <th>Eşya Vnum</th>
  <td class="text-center">'.$itemDetay->vnum.'</td>
  </tr>';
  $html .= '<tr>
  <th>Adet</th>
  <td class="text-center">'.$itemDetay->count.'</td>
  </tr>';
  $html .= '<tr>
  <th>Pozisyon</th>
  <td class="text-center">'.$itemDetay->pos.'</td>
  </tr>';
  if ($itemDetay->limitvalue0!=0) {
    if ($itemDetay->limitvalue0<121) {
      $html .= '<tr>
      <th>Seviye</th>
      <td class="text-center">'.$itemDetay->limitvalue0.'</td>
      </tr>';
    }
  }
  if ($itemDetay->value5>0 && $itemDetay->flag!="ITEM_STACKABLE") {
    if ($itemDetay->wearflag=="WEAR_SHIELD" || $itemDetay->wearflag=='WEAR_BODY' || $itemDetay->wearflag=='WEAR_FOOTS') {
      $html .= '<tr>
      <th>Defans</th>
      <td class="text-center">'.($itemDetay->value1+($itemDetay->value5*2)).'</td>
      </tr>';
    }
    if ($itemDetay->wearflag=="WEAR_WEAPON") {
      $html .= '<tr>
      <th>Saldırı Değeri</th>
      <td class="text-center">'.($itemDetay->value3+$itemDetay->value5).' - '.($itemDetay->value4+$itemDetay->value5).'</td>
      </tr>';
      $html .= '<tr>
      <th>Büyülü Saldırı Değeri</th>
      <td class="text-center">'.($itemDetay->value1+$itemDetay->value5).' - '.($itemDetay->value2+$itemDetay->value5).'</td>
      </tr>';
    }
  }
  for ($i=0; $i <=3 ; $i++) {
    $applytype = 'applytype'.$i;
    $applyvalue = 'applyvalue'.$i;
    if (isset($itemDetay->$applytype) && $itemDetay->$applytype!="") {
      if ($itemDetay->$applytype>0) {
        $applySearch = array_search($itemDetay->$applytype,array_column($efsunID, 'id'));
        if (isset($efsunID[$applySearch]->name)) {
          $efsun = $efsunID[$applySearch]->name;
        }else {
          $efsun = '*'.$itemDetay->$applytype.'*';
        }
        $html .= '<tr>
        <th>'.$efsun.'</th>
        <td class="text-center">'.$itemDetay->$applyvalue.'</td>
        </tr>';
      }
    }
  }
  for ($i=0; $i <= 6 ; $i++) {
    $attrtype = 'attrtype'.$i;
    $attrvalue = 'attrvalue'.$i;
    if (isset($itemDetay->$attrtype) && $itemDetay->$attrtype!=0) {
      $applySearch = array_search($itemDetay->$attrtype,array_column($efsunID, 'id'));
      if (isset($efsunID[$applySearch]->name)) {
        $efsun = $efsunID[$applySearch]->name;
      }else {
        $efsun = '*'.$itemDetay->$attrtype.'*';
      }
      $html .= '<tr>
      <th>'.$efsun.'</th>
      <td class="text-center">'.$itemDetay->$attrvalue.'</td>
      </tr>';
    }
  }
  for ($i=0; $i <=5 ; $i++) {
    $socket = 'socket'.$i;
    if (isset($itemDetay->$socket) && $itemDetay->$socket>1 && $i==0 && strlen($itemDetay->$socket)==10) {
      $html .= '<tr>
      <th>Bitiş Süresi</th>
      <td>'.DateDMYHMS(date('Y-m-d H:i:s',$itemDetay->$socket)).'</td>
      </tr>';
    }else if (isset($itemDetay->$socket) && $itemDetay->$socket>1 && isset($itemDetay->wearflag) && $itemDetay->wearflag!='WEAR_BODY' && $itemDetay->wearflag!='WEAR_WEAPON' && $i==0 && strlen($itemDetay->$socket)==5) {
      $html .= '<tr>
      <th>Bitiş Süresi</th>
      <td>'.$itemDetay->$socket.'</td>
      </tr>';
    }
    if (isset($itemDetay->$socket) && $itemDetay->$socket!=0 && isset($itemDetay->wearflag) && ($itemDetay->wearflag=='WEAR_BODY' || $itemDetay->wearflag=='WEAR_WEAPON') && strlen($itemDetay->$socket)==5) {
      $html .= '<tr>
      <yh>Ekli Taş</yh>
      <td>'.$itemDetay->$socket.'</td>
      </tr>';
    }
  }
  $html .= '</table>';
  return $html;
}
function SendMail($info=['to','subject','message'],$debug=false)
{
  $db                 = \Config\Database::connect();
  $ayarModel          = model('Ayar_model');
  $smtpGonderenIsim   = $ayarModel->AyarCek('smtpGonderenIsim',$db);
  $smtpHost           = $ayarModel->AyarCek('smtpHost',$db);
  $smtpEpostaAdresi   = $ayarModel->AyarCek('smtpEpostaAdresi',$db);
  $smtpEpostaSifresi  = $ayarModel->AyarCek('smtpEpostaSifresi',$db);
  $smtpPort           = $ayarModel->AyarCek('smtpPort',$db);
  $smtpGuvenlik       = $ayarModel->AyarCek('smtpGuvenlik',$db);

  $email = \Config\Services::email();

  $config['protocol']     = 'smtp';
  $config['SMTPHost']     = $smtpHost->setting_content;
  $config['SMTPUser']     = $smtpEpostaAdresi->setting_content;
  $config['SMTPPass']     = $smtpEpostaSifresi->setting_content;
  $config['SMTPPort']     = $smtpPort->setting_content;
  $config['SMTPTimeout']  = 10;
  if ($smtpGuvenlik->setting_content!="yok") {
    $config['SMTPCrypto'] = $smtpGuvenlik->setting_content;
  }
  $config['mailType']     = 'html';
  $config['charset']      = 'utf-8';
  $config['wordWrap']     = true;
  $config['newline']      = "\r\n";

  $email->initialize($config);
  if (isset($info['name'])) {
    $email->setFrom($smtpEpostaAdresi->setting_content,$info['name']);
  }else {
    $email->setFrom($smtpEpostaAdresi->setting_content,$smtpGonderenIsim->setting_content);
  }
  $email->setTo($info['to']);
  $email->setSubject($info['subject']);
  $mail_content = [
    'emailTitle'      => $info['subject'],
    'emailContent'    => $info['message'],
  ];
  $body = view('Email/Template',$mail_content);
  $email->setMessage($body);
  if ($debug==true) {
    $send = $email->send(false);
    print_r($email->printDebugger());
  }else {
    $send = $email->send();
  }
  if($send){
    return true;
  }else {
    return false;
  }
}
function MysqlPasswordHash($raw)
{
  return '*'.strtoupper(hash('sha1',pack('H*',hash('sha1', $raw))));
}
function KarakterTipi($job)
{
  switch ($job) {
    case 0:
    return lang('Genel.erkekSavasci');
    break;
    case 1:
    return lang('Genel.kadinNinja');
    break;
    case 2:
    return lang('Genel.erkekSura');
    break;
    case 3:
    return lang('Genel.kadinSaman');
    break;
    case 4:
    return lang('Genel.kadinSavasci');
    break;
    case 5:
    return lang('Genel.erkekNinja');
    break;
    case 6:
    return lang('Genel.kadinSura');
    break;
    case 7:
    return lang('Genel.erkekSaman');
    break;
    case 8:
    return lang('Genel.lycan');
    break;
  }
}
function SendServer($text, $type = "NOTICE", $port = 30004){
  if (p2pStatus==1) {
    // IP and ADMINPAGE_PASSWORD of your Metin2 server
    $addr = p2pHost; $pass = p2pPassword;
    // CREATE
    $socket = @socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    if ($socket < 0 || $socket === false){
      return false;
    }
    @socket_set_option($socket, SOL_SOCKET, SO_RCVTIMEO, ['sec'=>1,'usec'=>0]);
    @socket_set_option($socket, SOL_SOCKET, SO_SNDTIMEO, ['sec'=>1,'usec'=>0]);
    $result = @socket_connect($socket, $addr, $port);
    if ($result < 0 || $result === false){
      @socket_close($socket);
      return false;
    }
    if($type == "USER_COUNT") {
      $query = "\x40".$type."\x0A";
    }else {
      $query2 = "\x40".$pass."\x0A";
      $query_size2 = strlen($query2);
      $query_result2 = socket_write($socket, $query2, $query_size2);
      socket_recv($socket, $result2, 256, 0);
      $query = "\x40".$type." ".$text."\x0A";
    }
    $query_size = strlen($query);
    $query_result = socket_write($socket, $query, $query_size);
    if ($query_result < 0){
      return false;
    }else{
      $result1 = socket_recv($socket, $result2, 256, 0);
      if ($type == "USER_COUNT"){
        $count = trim($result2);
        $count = explode(' ', $count);
        return $count;
      }else{
        return "$result2\n";
      }
    }
    // CLOSE
    socket_close($socket);
  }else {
    return false;
  }
}
function EncryptDecrypt($string, $action)
{
  $output = false;
  $encrypt_method = "AES-256-CBC";
  $secret_key = 's:kz=*^,Y+AKoi+e^HdR2X?EUkEGJMXevQWgA)v4!^,*_EkdqQE1-=29JDd=Fjs*';
  $secret_iv = 'xNKYR8YJe},gY>hGh!=,KNsK.oF]>oB++2MqTCR}Q*xqwYU*U)#JQK?u5@Miqd5%';
  $key = hash('sha256', $secret_key);
  $iv = substr(hash('sha256', $secret_iv), 0, 16);
  if ( $action == 'encrypt' ) {
    $output = openssl_encrypt($string, $encrypt_method, $key, 0, $iv);
    $output = base64_encode($output);
  } else if( $action == 'decrypt' ) {
    $output = openssl_decrypt(base64_decode($string), $encrypt_method, $key, 0, $iv);
  }
  return $output;
}
function IsAllowedViewModule($moduleName="")
{
  $user_roles = session('user_role');
  if (session('is_admin')==true) {
    return true;
  }else {
    if (isset($user_roles->$moduleName)){
      return true;
    }else {
      return false;
    }
  }
}
function ConstantHeader()
{
  if (!GetFileCache('KullaniciBilgileri-'.session('user_id'))) {
    $db = \Config\Database::connect();
    $constantHeader['kullaniciBilgileri'] = model('Hesap_model')->KullaniciBilgileri(session('user_id'),$db);
    if (!$constantHeader['kullaniciBilgileri']) {
      header('Location: '.base_url('CikisYap'));
      exit;
    }else {
      session()->set('user_role',json_decode($constantHeader['kullaniciBilgileri']->user_role));
      session()->set('is_admin',($constantHeader['kullaniciBilgileri']->user_rank=="9"?true:false));
      CreateFileCache('KullaniciBilgileri-'.session('user_id'),$constantHeader['kullaniciBilgileri'],3600);
    }
  }else {
    $constantHeader['kullaniciBilgileri'] = GetFileCache('KullaniciBilgileri-'.session('user_id'));
  }
  if ($constantHeader['kullaniciBilgileri']->user_end_session=="1") {
    $girisYapModel  = model('Giris_yap_model');
    $db             = \Config\Database::connect();
    $updateData     = [
      'user_end_session' => "0"
    ];
    $result = $girisYapModel->Guncelle($updateData,session('user_id'),$db);
    if ($result) {
      DeleteFileCache('KullaniciBilgileri-'.session('user_id'));
      header('Location: '.base_url('CikisYap'));
      exit;
    }
  }
  if (time()>(strtotime($constantHeader['kullaniciBilgileri']->user_login_date)+600)) {
    $girisYapModel  = model('Giris_yap_model');
    $db             = \Config\Database::connect();
    $updateData     = [
      'user_login_date' => date('Y-m-d H:i:s')
    ];
    $girisYapModel->Guncelle($updateData,session('user_id'),$db);
    DeleteFileCache('KullaniciBilgileri-'.session('user_id'));
  }
  if ($constantHeader['kullaniciBilgileri']->user_status=="0") {
    header('Location: '.base_url('CikisYap'));
    exit;
  }
  $anasayfaModel  = model('Anasayfa_model');
  $constantHeader['ayarSiteAdi']            = $anasayfaModel->AyarCek('siteAdi');
  $constantHeader['ayarFooterYazisi']       = $anasayfaModel->AyarCek('footerYazisi');
  $constantHeader['ayarJavascriptKodlari']  = $anasayfaModel->AyarCek('javascriptKodlari');
  return $constantHeader;
}
function LogAdd($content="",$link="#",$user=0)
{
  $islemKayitModel = model('Islem_kayit_model');
  $logAddData  = [
    'log_user_id' => $user,
    'log_content' => $content,
    'log_link'    => $link,
    'log_status'  => "0",
    'log_date'    => date('Y-m-d H:i:s'),
    'log_ip'      => GetRealIpAddress(),
  ];
  $result = $islemKayitModel->Ekle($logAddData);
  if ($result) {
    return true;
  }else {
    return false;
  }
}
function RememberMeCheck()
{
  helper('cookie');
  $girisYapModel = model('Giris_yap_model');
  if (get_cookie(cookieKey,true) && !session('user_id')){
    if (EncryptDecrypt(get_cookie(cookieKey,true),'decrypt')) {
      $db       = \Config\Database::connect();
      $response = $girisYapModel->BeniHatirlaTokenKontrol(get_cookie(cookieKey,true),$db);
      if ($response){
        session()->set('user_role',json_decode($response->user_role));
        session()->set('user_id',$response->user_id);
        session()->set('is_admin',($response->user_rank=="9"?true:false));
      }else{
        setcookie(cookieKey,"",-1,'/','');
      }
    }else {
      setcookie(cookieKey,"",-1,'/','');
    }
  }
}
function CreateToken($type,$db)
{
  helper('text');
  if ($type=="BeniHatirla") {
    $girisYapModel  = model('Giris_yap_model');
    $token          = EncryptDecrypt(random_string('alpha', 16),'encrypt');
    $check          = $girisYapModel->BeniHatirlaTokenKontrol($token,$db);
  }
  if ($check) {
    CreateToken($type,$db);
  }else {
    return $token;
  }
}
function MultiDeleteFileCache($fileCacheName)
{
  foreach (glob(FCPATH.'writable/cache/'.$fileCacheName."*") as $filename) {
    unlink($filename);
  }
}
function DeleteFileCache($fileCacheName)
{
  cache()->delete($fileCacheName);
}
function GetFileCache($fileCacheName)
{
  return cache($fileCacheName);
}
function CreateFileCache($fileCacheName,$data,$time=600)
{
  cache()->save($fileCacheName,$data,$time);
}
function TimeAgo($zaman)
{
  $zaman =  strtotime($zaman);
  $zaman_farki = time() - $zaman;
  $saniye = $zaman_farki;
  $dakika = round($zaman_farki/60);
  $saat = round($zaman_farki/3600);
  $gun = round($zaman_farki/86400);
  $hafta = round($zaman_farki/604800);
  $ay = round($zaman_farki/2419200);
  $yil = round($zaman_farki/29030400);
  if($saniye<60){
    if($saniye==0){
      return lang('Genel.timeAgo.azOnce');
    }else {
      return $saniye.lang('Genel.timeAgo.saniyeOnce');
    }
  }else if($dakika<60){
    return $dakika.lang('Genel.timeAgo.dakikaOnce');
  }else if($saat<24){
    return $saat.lang('Genel.timeAgo.saatOnce');
  }else if($gun<7){
    return $gun.lang('Genel.timeAgo.gunOnce');
  }else if($hafta<4){
    return $hafta.lang('Genel.timeAgo.haftaOnce');
  }else if($ay<12){
    return $ay.lang('Genel.timeAgo.ayOnce');
  }else{
    return $yil.lang('Genel.timeAgo.yilOnce');
  }
}
function GetRealIpAddress()
{
  $ipAddress = null;
  if (isset($_SERVER['HTTP_CF_CONNECTING_IP']))
  $ipAddress = $_SERVER['HTTP_CF_CONNECTING_IP'];
  else if (isset($_SERVER['HTTP_CLIENT_IP']))
  $ipAddress = $_SERVER['HTTP_CLIENT_IP'];
  else if(isset($_SERVER['HTTP_X_FORWARDED_FOR']))
  $ipAddress = $_SERVER['HTTP_X_FORWARDED_FOR'];
  else if(isset($_SERVER['HTTP_X_FORWARDED']))
  $ipAddress = $_SERVER['HTTP_X_FORWARDED'];
  else if(isset($_SERVER['HTTP_X_CLUSTER_CLIENT_IP']))
  $ipAddress = $_SERVER['HTTP_X_CLUSTER_CLIENT_IP'];
  else if(isset($_SERVER['HTTP_FORWARDED_FOR']))
  $ipAddress = $_SERVER['HTTP_FORWARDED_FOR'];
  else if(isset($_SERVER['HTTP_FORWARDED']))
  $ipAddress = $_SERVER['HTTP_FORWARDED'];
  else if(isset($_SERVER['REMOTE_ADDR']))
  $ipAddress = $_SERVER['REMOTE_ADDR'];
  else
  $ipAddress = 'UNKNOWN';
  return esc($ipAddress);
}
function WebTitle($value)
{
  if (in_array($value,service('uri')->getSegments())) {
    return true;
  }else {
    return false;
  }
}
function DateDMYHMS($date)
{
  if ($date==0) {
    return false;
  }else {
    return iconv('UTF-8','UTF-8',strftime(' %d %B %Y %H:%M:%S',strtotime($date)));
  }
}
function DateDMYHM($date)
{
  if ($date==0) {
    return false;
  }else {
    return iconv('UTF-8','UTF-8',strftime(' %d %B %Y %H:%M',strtotime($date)));
  }
}
function DateDMY($date)
{
  if ($date==0) {
    return false;
  }else {
    return iconv('UTF-8','UTF-8',strftime(' %d %B %Y ',strtotime($date)));
  }
}
function DateDM($date)
{
  if ($date==0) {
    return false;
  }else {
    return iconv('UTF-8','UTF-8',strftime(' %d %B ',strtotime($date)));
  }
}
function SunucuKomutHizli($text, $type = "RELOAD"){
  if (p2pStatus!=1) {
    return false;
  }
  foreach ((array)p2pPorts as $port) {
    $fp = @stream_socket_client('tcp://'.p2pHost.':'.$port, $errno, $errstr, 0.5);
    if (!$fp) {
      continue;
    }
    @stream_set_timeout($fp, 1);
    @fwrite($fp, "\x40".p2pPassword."\x0A\x40".$type." ".$text."\x0A");
    @fclose($fp);
  }
}
function ResponseResult($type,$message,$response=[])
{
  if ($type==='success' && p2pStatus==1) {
    $controller = '';
    if (function_exists('service')) {
      $router = \Config\Services::router();
      $controller = $router ? $router->controllerName() : '';
    }
    $yenilenecekler = ['Esya','Canavar','Sandik','Biyolog','NPC','Efsun','Yukseltme','Cark','Balikcilik','NesneMarket','GM'];
    foreach ($yenilenecekler as $modul) {
      if (stripos($controller,'\\'.$modul)!==false || str_ends_with($controller,$modul)) {
        SunucuKomutHizli('P',"RELOAD");
        SunucuKomutHizli('I',"RELOAD");
        break;
      }
    }
  }
  $response['type']=$type;
  if (is_array($message)) {
    $response[$type]=implode('<br>',$message);
  }else {
    $response[$type]=$message;
  }
  echo json_encode($response);
  exit;
}
function Permalink($str, $options = array())
{
  $str = mb_convert_encoding((string)$str, 'UTF-8', mb_list_encodings());
  $defaults = array(
    'delimiter' => '-',
    'limit' => null,
    'lowercase' => true,
    'replacements' => array(),
    'transliterate' => true
  );
  $options = array_merge($defaults, $options);
  $char_map = array(
    // Latin
    'À' => 'A', 'Á' => 'A', 'Â' => 'A', 'Ã' => 'A', 'Ä' => 'A', 'Å' => 'A', 'Æ' => 'AE', 'Ç' => 'C',
    'È' => 'E', 'É' => 'E', 'Ê' => 'E', 'Ë' => 'E', 'Ì' => 'I', 'Í' => 'I', 'Î' => 'I', 'Ï' => 'I',
    'Ð' => 'D', 'Ñ' => 'N', 'Ò' => 'O', 'Ó' => 'O', 'Ô' => 'O', 'Õ' => 'O', 'Ö' => 'O', 'Ő' => 'O',
    'Ø' => 'O', 'Ù' => 'U', 'Ú' => 'U', 'Û' => 'U', 'Ü' => 'U', 'Ű' => 'U', 'Ý' => 'Y', 'Þ' => 'TH',
    'ß' => 'ss',
    'à' => 'a', 'á' => 'a', 'â' => 'a', 'ã' => 'a', 'ä' => 'a', 'å' => 'a', 'æ' => 'ae', 'ç' => 'c',
    'è' => 'e', 'é' => 'e', 'ê' => 'e', 'ë' => 'e', 'ì' => 'i', 'í' => 'i', 'î' => 'i', 'ï' => 'i',
    'ð' => 'd', 'ñ' => 'n', 'ò' => 'o', 'ó' => 'o', 'ô' => 'o', 'õ' => 'o', 'ö' => 'o', 'ő' => 'o',
    'ø' => 'o', 'ù' => 'u', 'ú' => 'u', 'û' => 'u', 'ü' => 'u', 'ű' => 'u', 'ý' => 'y', 'þ' => 'th',
    'ÿ' => 'y',
    // Latin symbols
    '©' => '(c)',
    // Greek
    'Α' => 'A', 'Β' => 'B', 'Γ' => 'G', 'Δ' => 'D', 'Ε' => 'E', 'Ζ' => 'Z', 'Η' => 'H', 'Θ' => '8',
    'Ι' => 'I', 'Κ' => 'K', 'Λ' => 'L', 'Μ' => 'M', 'Ν' => 'N', 'Ξ' => '3', 'Ο' => 'O', 'Π' => 'P',
    'Ρ' => 'R', 'Σ' => 'S', 'Τ' => 'T', 'Υ' => 'Y', 'Φ' => 'F', 'Χ' => 'X', 'Ψ' => 'PS', 'Ω' => 'W',
    'Ά' => 'A', 'Έ' => 'E', 'Ί' => 'I', 'Ό' => 'O', 'Ύ' => 'Y', 'Ή' => 'H', 'Ώ' => 'W', 'Ϊ' => 'I',
    'Ϋ' => 'Y',
    'α' => 'a', 'β' => 'b', 'γ' => 'g', 'δ' => 'd', 'ε' => 'e', 'ζ' => 'z', 'η' => 'h', 'θ' => '8',
    'ι' => 'i', 'κ' => 'k', 'λ' => 'l', 'μ' => 'm', 'ν' => 'n', 'ξ' => '3', 'ο' => 'o', 'π' => 'p',
    'ρ' => 'r', 'σ' => 's', 'τ' => 't', 'υ' => 'y', 'φ' => 'f', 'χ' => 'x', 'ψ' => 'ps', 'ω' => 'w',
    'ά' => 'a', 'έ' => 'e', 'ί' => 'i', 'ό' => 'o', 'ύ' => 'y', 'ή' => 'h', 'ώ' => 'w', 'ς' => 's',
    'ϊ' => 'i', 'ΰ' => 'y', 'ϋ' => 'y', 'ΐ' => 'i',
    // Turkish
    'Ş' => 'S', 'İ' => 'I', 'Ç' => 'C', 'Ü' => 'U', 'Ö' => 'O', 'Ğ' => 'G',
    'ş' => 's', 'ı' => 'i', 'ç' => 'c', 'ü' => 'u', 'ö' => 'o', 'ğ' => 'g',
    // Russian
    'А' => 'A', 'Б' => 'B', 'В' => 'V', 'Г' => 'G', 'Д' => 'D', 'Е' => 'E', 'Ё' => 'Yo', 'Ж' => 'Zh',
    'З' => 'Z', 'И' => 'I', 'Й' => 'J', 'К' => 'K', 'Л' => 'L', 'М' => 'M', 'Н' => 'N', 'О' => 'O',
    'П' => 'P', 'Р' => 'R', 'С' => 'S', 'Т' => 'T', 'У' => 'U', 'Ф' => 'F', 'Х' => 'H', 'Ц' => 'C',
    'Ч' => 'Ch', 'Ш' => 'Sh', 'Щ' => 'Sh', 'Ъ' => '', 'Ы' => 'Y', 'Ь' => '', 'Э' => 'E', 'Ю' => 'Yu',
    'Я' => 'Ya',
    'а' => 'a', 'б' => 'b', 'в' => 'v', 'г' => 'g', 'д' => 'd', 'е' => 'e', 'ё' => 'yo', 'ж' => 'zh',
    'з' => 'z', 'и' => 'i', 'й' => 'j', 'к' => 'k', 'л' => 'l', 'м' => 'm', 'н' => 'n', 'о' => 'o',
    'п' => 'p', 'р' => 'r', 'с' => 's', 'т' => 't', 'у' => 'u', 'ф' => 'f', 'х' => 'h', 'ц' => 'c',
    'ч' => 'ch', 'ш' => 'sh', 'щ' => 'sh', 'ъ' => '', 'ы' => 'y', 'ь' => '', 'э' => 'e', 'ю' => 'yu',
    'я' => 'ya',
    // Ukrainian
    'Є' => 'Ye', 'І' => 'I', 'Ї' => 'Yi', 'Ґ' => 'G',
    'є' => 'ye', 'і' => 'i', 'ї' => 'yi', 'ґ' => 'g',
    // Czech
    'Č' => 'C', 'Ď' => 'D', 'Ě' => 'E', 'Ň' => 'N', 'Ř' => 'R', 'Š' => 'S', 'Ť' => 'T', 'Ů' => 'U',
    'Ž' => 'Z',
    'č' => 'c', 'ď' => 'd', 'ě' => 'e', 'ň' => 'n', 'ř' => 'r', 'š' => 's', 'ť' => 't', 'ů' => 'u',
    'ž' => 'z',
    // Polish
    'Ą' => 'A', 'Ć' => 'C', 'Ę' => 'e', 'Ł' => 'L', 'Ń' => 'N', 'Ó' => 'o', 'Ś' => 'S', 'Ź' => 'Z',
    'Ż' => 'Z',
    'ą' => 'a', 'ć' => 'c', 'ę' => 'e', 'ł' => 'l', 'ń' => 'n', 'ó' => 'o', 'ś' => 's', 'ź' => 'z',
    'ż' => 'z',
    // Latvian
    'Ā' => 'A', 'Č' => 'C', 'Ē' => 'E', 'Ģ' => 'G', 'Ī' => 'i', 'Ķ' => 'k', 'Ļ' => 'L', 'Ņ' => 'N',
    'Š' => 'S', 'Ū' => 'u', 'Ž' => 'Z',
    'ā' => 'a', 'č' => 'c', 'ē' => 'e', 'ģ' => 'g', 'ī' => 'i', 'ķ' => 'k', 'ļ' => 'l', 'ņ' => 'n',
    'š' => 's', 'ū' => 'u', 'ž' => 'z'
  );
  $str = preg_replace(array_keys($options['replacements']), $options['replacements'], $str);
  if ($options['transliterate']) {
    $str = str_replace(array_keys($char_map), $char_map, $str);
  }
  $str = preg_replace('/[^\p{L}\p{Nd}]+/u', $options['delimiter'], $str);
  $str = preg_replace('/(' . preg_quote($options['delimiter'], '/') . '){2,}/', '$1', $str);
  $str = mb_substr($str, 0, ($options['limit'] ? $options['limit'] : mb_strlen($str, 'UTF-8')), 'UTF-8');
  $str = trim($str, $options['delimiter']);
  return $options['lowercase'] ? mb_strtolower($str, 'UTF-8') : $str;
}
