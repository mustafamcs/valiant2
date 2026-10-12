<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class NesneMarket extends BaseController
{
  public $viewFolder        = "";
  public $nesneMarketModel  = "";

  public function __construct()
  {
    $this->viewFolder       = "NesneMarket";
    $this->nesneMarketModel = model('Nesne_market_model');
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function Kategori()
  {
    if (!IsAllowedViewModule('nesneMarketKategoriGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Kategori",$viewData);
  }

  public function KategoriAjax()
  {
    if (!IsAllowedViewModule('nesneMarketKategoriGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $siralama = ['cat_id','cat_name','cat_main_id'];
    if ($request->getPost('search[value]')) {
      $yaz = $this->nesneMarketModel->KategoriAjaxAra($request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }else{
      $yaz = $this->nesneMarketModel->KategoriAjax($request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->cat_id;
      if ($value->cat_main_id!=255) {
        $ustKategori = $this->nesneMarketModel->KategoriKontrolCache($value->cat_main_id);
        if (isset($ustKategori->cat_name)) {
          $sub_array[] = mb_convert_encoding($ustKategori->cat_name, 'UTF-8' ,"ISO-8859-9");
        }else {
          $sub_array[] = $value->cat_main_id;
        }
      }else {
        $sub_array[] = '-';
      }
      $sub_array[] = mb_convert_encoding($value->cat_name, 'UTF-8' ,"ISO-8859-9");
      if (IsAllowedViewModule('nesneMarketKategoriDuzenleyebilsin') || IsAllowedViewModule('nesneMarketKategoriSilebilsin')) {
        $buttons = "";
        if (IsAllowedViewModule('nesneMarketKategoriDuzenleyebilsin')) {
          $buttons .= '<a class="btn btn-primary pt-1 pb-1 ps-2 pe-2" data-bs-toggle="modal" data-bs-target="#duzenle" href="javascript:void(0)" data-id="'.$value->cat_id.'">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 7h-3a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-3" /><path d="M9 15h3l8.5 -8.5a1.5 1.5 0 0 0 -3 -3l-8.5 8.5v3" /><line x1="16" y1="5" x2="19" y2="8" /></svg>
          </a>';
        }
        if (IsAllowedViewModule('nesneMarketKategoriSilebilsin')) {
          $buttons .= '<a class="btn btn-danger pt-1 pb-1 ps-2 pe-2 ms-2 kategoriSil" href="javascript:void(0)" data-id="'.$value->cat_id.'" data-header="'.lang('Genel.silBaslik').'" data-message="'.lang('Genel.buIslemGeriAlinamaz').'" data-yes="'.lang('Genel.evet').'" data-no="'.lang('Genel.hayir').'">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><line x1="4" y1="7" x2="20" y2="7" /><line x1="10" y1="11" x2="10" y2="17" /><line x1="14" y1="11" x2="14" y2="17" /><path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12" /><path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3" /></svg>
          </a>';
        }
        $sub_array[] = $buttons;
      }
      $data[] = $sub_array;
    }
    $output = array(
      "draw"            =>  intval($_POST["draw"]),
      "recordsFiltered" =>  (count($yaz)==$request->getPost('length')?$request->getPost('start')+$request->getPost('length')+1:0),
      "data"            =>  $data
    );
    echo json_encode($output, JSON_INVALID_UTF8_SUBSTITUTE);
    exit;
  }

  public function UstKategoriler()
  {
    if (IsAllowedViewModule('nesneMarketKategoriEkleyebilsin')) {
      $request  = \Config\Services::request();
      $search   = $request->getGet('q');
      if (!$search) {
        $search = "";
      }
      $kategoriler = $this->nesneMarketModel->KategoriAra($search);
      $data[] = [
        'id'    => 255,
        'text'  => "Yok",
      ];
      foreach ($kategoriler as $key => $value) {
        if ($value->cat_main_id==255) {
          $data[] = [
            'id'    => $value->cat_id,
            'text'  => mb_convert_encoding($value->cat_name, 'UTF-8' ,"ISO-8859-9")
          ];
        }
      }
      echo json_encode($data);
      exit;
    }
  }

  public function KategoriEkle()
  {
    if (!IsAllowedViewModule('nesneMarketKategoriEkleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'cat_main_id' => ['label' => lang('NesneMarket.sayfa.ustKategori'), 'rules' => "required|integer"],
      'cat_name'    => ['label' => lang('NesneMarket.sayfa.kategoriAdi'), 'rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db = \Config\Database::connect('metin2');
      if ($request->getPost('cat_main_id')!=255) {
        $kontrol  = $this->nesneMarketModel->KategoriKontrol($request->getPost('cat_main_id'),$db);
        if (!$kontrol) {
          responseResult('error',lang('NesneMarket.cikti.ustKategoriYok'));
        }else if ($kontrol->cat_main_id!=255) {
          responseResult('error',lang('NesneMarket.cikti.ustKategoriYok'));
        }
      }
      $data = [
        'cat_name'    =>  mb_convert_encoding($request->getPost('cat_name'), 'ISO-8859-9' ,"UTF-8"),
        'cat_main_id' =>  $request->getPost('cat_main_id'),
      ];
      $result = $this->nesneMarketModel->KategoriEkle($data,$db);
      if ($result) {
        LogAdd(lang('NesneMarket.kayit.kategoriEklendi',[ 'name' => $request->getPost('cat_name') ]),'NesneMarket/Kategori',session('user_id'));
        responseResult('success',lang('NesneMarket.cikti.kategoriEklendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function KategoriDetay($id=0)
  {
    if (!IsAllowedViewModule('nesneMarketKategoriDuzenleyebilsin')) {
      responseResult('error',lang('Genel.yetkinYok'));
    }
    $request  = \Config\Services::request();
    $db       = \Config\Database::connect('metin2');
    $kontrol  = $this->nesneMarketModel->KategoriKontrol($id,$db);
    if (!$kontrol) {
      responseResult('error',lang('NesneMarket.sayfa.kategoriYok'));
    }else {
      $returnData['cat_name'] = mb_convert_encoding($kontrol->cat_name, 'UTF-8' ,"ISO-8859-9");
      if ($kontrol->cat_main_id!=255) {
        $ustKategori = $this->nesneMarketModel->KategoriKontrol($kontrol->cat_main_id,$db);
        if (isset($ustKategori->cat_name)) {
          $returnData['cat_main_id']['name']  = mb_convert_encoding($ustKategori->cat_name, 'UTF-8' ,"ISO-8859-9");
          $returnData['cat_main_id']['id']    = $kontrol->cat_main_id;
        }else {
          $returnData['cat_main_id']['name']  = "Yok";
          $returnData['cat_main_id']['id']    = $kontrol->cat_main_id;
        }
      }else {
        $returnData['cat_main_id']['name']  = "Yok";
        $returnData['cat_main_id']['id']    = $kontrol->cat_main_id;
      }
      $returnData['cat_id']   = $kontrol->cat_id;
      echo json_encode($returnData);
      exit;
    }
  }

  public function KategoriDuzenle()
  {
    if (!IsAllowedViewModule('nesneMarketKategoriDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'cat_main_id' => ['label' => lang('NesneMarket.sayfa.ustKategori'), 'rules' => "required|integer"],
      'cat_name'    => ['label' => lang('NesneMarket.sayfa.kategoriAdi'), 'rules' => "required"],
      'cat_id'      => ['label' => lang('NesneMarket.sayfa.kategoriAdi'), 'rules' => "required|integer"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->nesneMarketModel->KategoriKontrol($request->getPost('cat_id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('NesneMarket.cikti.kategoriYok'));
      }
      if ($request->getPost('cat_main_id')!=255) {
        $ustKategoriKontrol  = $this->nesneMarketModel->KategoriKontrol($request->getPost('cat_main_id'),$db);
        if (!$ustKategoriKontrol) {
          responseResult('error',lang('NesneMarket.cikti.ustKategoriYok'));
        }else if ($ustKategoriKontrol->cat_main_id!=255) {
          responseResult('error',lang('NesneMarket.cikti.ustKategoriYok'));
        }
      }
      $data = [
        'cat_name'    =>  mb_convert_encoding($request->getPost('cat_name'), 'ISO-8859-9' ,"UTF-8"),
        'cat_main_id' =>  $request->getPost('cat_main_id'),
      ];
      $result = $this->nesneMarketModel->KategoriGuncelle($data,$kontrol->cat_id,$db);
      if ($result) {
        DeleteFileCache('KategoriKontrol-'.$kontrol->cat_id);
        LogAdd(lang('NesneMarket.kayit.kategoriDuzenlendi',[ 'name' => mb_convert_encoding($kontrol->cat_name, 'UTF-8' ,"ISO-8859-9") ]),'NesneMarket/Kategori',session('user_id'));
        responseResult('success',lang('NesneMarket.cikti.kategoriDuzenlendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function KategoriSil()
  {
    if (!IsAllowedViewModule('nesneMarketKategoriSilebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'cat_id'  => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->nesneMarketModel->KategoriKontrol($request->getPost('cat_id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('NesneMarket.sayfa.kategoriYok'));
      }else {
        $result = $this->nesneMarketModel->KategoriSil($kontrol->cat_id,$db);
        if ($result) {
          DeleteFileCache('KategoriKontrol-'.$kontrol->cat_id);
          LogAdd(lang('NesneMarket.kayit.kategoriSilindi',[ 'name' => mb_convert_encoding($kontrol->cat_name, 'UTF-8' ,"ISO-8859-9") ]),'NesneMarket/Kategori',session('user_id'));
          responseResult('success',lang('NesneMarket.cikti.kategoriSilindi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Index()
  {
    if (!IsAllowedViewModule('nesneMarketEsyaGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    $viewData['efsunlar'] = $this->nesneMarketModel->Efsunlar();
    return view("{$this->viewFolder}/Index",$viewData);
  }

  public function Ajax()
  {
    if (!IsAllowedViewModule('nesneMarketEsyaGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $siralama = ['id','vnum','price','category_id','sell_count','status'];
    if ($request->getPost('search[value]')) {
      $yaz = $this->nesneMarketModel->AjaxAra($request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }else{
      $yaz = $this->nesneMarketModel->Ajax($request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->id;
      $itemIcon = $this->nesneMarketModel->ItemIcon($value->vnum);
      if (!empty($itemIcon) && $itemIcon!="-") {
        $sub_array[] = '<img src="'.base_url('assets/img/icon/'.$itemIcon->icon).'" title="'.$value->vnum.'"> '.mb_convert_encoding($value->item_name, 'UTF-8' ,"ISO-8859-9");
      }else {
        $sub_array[] = mb_convert_encoding($value->item_name, 'UTF-8' ,"ISO-8859-9");
      }
      $sub_array[] = $value->price;
      if (isset($value->cat_name)) {
        $sub_array[] = mb_convert_encoding($value->cat_name, 'UTF-8' ,"ISO-8859-9");
      }else {
        $sub_array[] = $value->category_id;
      }
      $sub_array[] = $value->sell_count;
      $sub_array[] = '<label class="form-check form-switch status_update" style="margin-top:2px;" data-id="'.$value->id.'"><input class="form-check-input" style="background-size: 1.5rem;" type="checkbox" '.($value->status=="1"?'checked':false).'></label>';
      if (IsAllowedViewModule('nesneMarketEsyaDuzenleyebilsin') || IsAllowedViewModule('nesneMarketEsyaSilebilsin')) {
        $buttons = "";
        if (IsAllowedViewModule('nesneMarketEsyaDuzenleyebilsin')) {
          $buttons .= '<a class="btn btn-primary pt-1 pb-1 ps-2 pe-2" data-bs-toggle="modal" data-bs-target="#duzenle" href="javascript:void(0)" data-id="'.$value->id.'">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 7h-3a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-3" /><path d="M9 15h3l8.5 -8.5a1.5 1.5 0 0 0 -3 -3l-8.5 8.5v3" /><line x1="16" y1="5" x2="19" y2="8" /></svg>
          </a>';
        }
        if (IsAllowedViewModule('nesneMarketEsyaSilebilsin')) {
          $buttons .= '<a class="btn btn-danger pt-1 pb-1 ps-2 pe-2 ms-2 esyaSil" href="javascript:void(0)" data-id="'.$value->id.'" data-header="'.lang('Genel.silBaslik').'" data-message="'.lang('Genel.buIslemGeriAlinamaz').'" data-yes="'.lang('Genel.evet').'" data-no="'.lang('Genel.hayir').'">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><line x1="4" y1="7" x2="20" y2="7" /><line x1="10" y1="11" x2="10" y2="17" /><line x1="14" y1="11" x2="14" y2="17" /><path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12" /><path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3" /></svg>
          </a>';
        }
        $sub_array[] = $buttons;
      }
      $data[] = $sub_array;
    }
    $output = array(
      "draw"            =>  intval($_POST["draw"]),
      "recordsFiltered" =>  (count($yaz)==$request->getPost('length')?$request->getPost('start')+$request->getPost('length')+1:0),
      "data"            =>  $data
    );
    echo json_encode($output, JSON_INVALID_UTF8_SUBSTITUTE);
    exit;
  }

  public function Kategoriler()
  {
    if (IsAllowedViewModule('nesneMarketEsyaEkleyebilsin')) {
      $request  = \Config\Services::request();
      $search   = $request->getGet('q');
      if (!$search) {
        $search = "";
      }
      $kategoriler = $this->nesneMarketModel->KategoriAra($search);
      $data[] = [
        'id'    => 0,
        'text'  => "Seçiniz",
      ];
      foreach ($kategoriler as $key => $value) {
        $data[] = [
          'id'    => $value->cat_id,
          'text'  => mb_convert_encoding($value->cat_name, 'UTF-8' ,"ISO-8859-9")
        ];
      }
      echo json_encode($data);
      exit;
    }
  }

  public function Ekle()
  {
    if (!IsAllowedViewModule('nesneMarketEsyaEkleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'category_id' => ['label' => lang('Genel.kategori'),  'rules' => "required|integer"],
      'vnum'        => ['label' => lang('Genel.esya'),      'rules' => "required|integer"],
      'item_name'   => ['label' => lang('Genel.esya'),      'rules' => "required"],
      'price'       => ['label' => lang('Genel.fiyat'),     'rules' => "required|integer"],
      'count'       => ['label' => lang('Genel.adet'),      'rules' => "required|integer"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db               = \Config\Database::connect('metin2');
      $kategoriKontrol  = $this->nesneMarketModel->KategoriKontrol($request->getPost('category_id'),$db);
      if (!$kategoriKontrol) {
        responseResult('error',lang('NesneMarket.cikti.kategoriYok'));
      }
      $esyaKontrol  = $this->nesneMarketModel->ItemProtoKontrol($request->getPost('vnum'),$db);
      if (!$esyaKontrol) {
        responseResult('error',lang('Esya.cikti.esyaYok'));
      }
      $data = [
        'category_id' =>  $kategoriKontrol->cat_id,
        'vnum'        =>  $esyaKontrol->vnum,
        'item_name'   =>  mb_convert_encoding($request->getPost('item_name'), 'ISO-8859-9' ,"UTF-8"),
        'price'       =>  $request->getPost('price'),
        'count'       =>  $request->getPost('count'),
        'time_type'   =>  $request->getPost('time_type'),
        'price_type'  =>  $request->getPost('price_type'),
        'socket0'     =>  $request->getPost('socket0'),
        'socket1'     =>  $request->getPost('socket1'),
        'socket2'     =>  $request->getPost('socket2'),
        'socket3'     =>  $request->getPost('socket3'),
        'attrtype0'   =>  $request->getPost('attrtype0'),
        'attrvalue0'  =>  $request->getPost('attrvalue0'),
        'attrtype1'   =>  $request->getPost('attrtype1'),
        'attrvalue1'  =>  $request->getPost('attrvalue1'),
        'attrtype2'   =>  $request->getPost('attrtype2'),
        'attrvalue2'  =>  $request->getPost('attrvalue2'),
        'attrtype3'   =>  $request->getPost('attrtype3'),
        'attrvalue3'  =>  $request->getPost('attrvalue3'),
        'attrtype4'   =>  $request->getPost('attrtype4'),
        'attrvalue4'  =>  $request->getPost('attrvalue4'),
        'attrtype5'   =>  $request->getPost('attrtype5'),
        'attrvalue5'  =>  $request->getPost('attrvalue5'),
        'attrtype6'   =>  $request->getPost('attrtype6'),
        'attrvalue6'  =>  $request->getPost('attrvalue6'),
        'status'      =>  $request->getPost('status'),
      ];
      $result = $this->nesneMarketModel->Ekle($data,$db);
      if ($result) {
        LogAdd(lang('NesneMarket.kayit.esyaEklendi',[ 'category' => mb_convert_encoding($kategoriKontrol->cat_name, 'UTF-8' ,"ISO-8859-9"), 'name' => $request->getPost('item_name') ]),'NesneMarket/Index',session('user_id'));
        responseResult('success',lang('NesneMarket.cikti.esyaEklendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Durum()
  {
    if (!IsAllowedViewModule('nesneMarketEsyaDuzenleyebilsin')) {
      responseResult('error',lang('Genel.yetkinYok'));
    }
    $validation =  \Config\Services::validation();
    $request    =  \Config\Services::request();
    $validation->setRules([
      'id' => ['rules'=> "required|integer"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db      = \Config\Database::connect('metin2');
      $kontrol = $this->nesneMarketModel->Kontrol($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Esya.cikti.esyaYok'));
      }else {
        if ($kontrol->status=="1") {
          $status = "0";
          $text = lang('NesneMarket.kayit.esyaDurumPasif',['name' => mb_convert_encoding($kontrol->item_name, 'UTF-8' ,"ISO-8859-9") ]);
        }else {
          $status = "1";
          $text = lang('NesneMarket.kayit.esyaDurumAktif',['name' => mb_convert_encoding($kontrol->item_name, 'UTF-8' ,"ISO-8859-9") ]);
        }
        $data = [
          'status' => $status,
        ];
        $response = $this->nesneMarketModel->Guncelle($data,$kontrol->id,$db);
        if ($response) {
          LogAdd($text,'NesneMarket/Index',session('user_id'));
          responseResult('success',$text);
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Detay($id=0)
  {
    if (!IsAllowedViewModule('nesneMarketEsyaDuzenleyebilsin')) {
      responseResult('error',lang('Genel.yetkinYok'));
    }
    $request  = \Config\Services::request();
    $db       = \Config\Database::connect('metin2');
    $kontrol  = $this->nesneMarketModel->Kontrol($id,$db);
    if (!$kontrol) {
      responseResult('error',lang('Esya.sayfa.esyaYok'));
    }else {
      $ustKategori = $this->nesneMarketModel->KategoriKontrol($kontrol->category_id,$db);
      if (isset($ustKategori->cat_name)) {
        $returnData['category_id']['name']  = mb_convert_encoding($ustKategori->cat_name, 'UTF-8' ,"ISO-8859-9");
        $returnData['category_id']['id']    = $kontrol->category_id;
      }else {
        $returnData['category_id']['name']  = "Yok";
        $returnData['category_id']['id']    = $kontrol->category_id;
      }
      $itemKontrol = $this->nesneMarketModel->ItemProtoKontrol($kontrol->vnum,$db);
      if (isset($itemKontrol->locale_name)) {
        $returnData['vnum']['name']  = mb_convert_encoding($itemKontrol->locale_name, 'UTF-8' ,"ISO-8859-9");
        $returnData['vnum']['id']    = $kontrol->vnum;
      }else {
        $returnData['vnum']['name']  = "Yok";
        $returnData['vnum']['id']    = $kontrol->vnum;
      }
      $returnData['item_name']    = mb_convert_encoding($kontrol->item_name, 'UTF-8' ,"ISO-8859-9");
      $returnData['price']        = $kontrol->price;
      $returnData['count']        = $kontrol->count;
      $returnData['time_type']    = $kontrol->time_type;
      $returnData['price_type']   = $kontrol->price_type;
      $returnData['socket0']      = $kontrol->socket0;
      $returnData['socket1']      = $kontrol->socket1;
      $returnData['socket2']      = $kontrol->socket2;
      $returnData['socket3']      = $kontrol->socket3;
      $returnData['attrtype0']    = $kontrol->attrtype0;
      $returnData['attrvalue0']   = $kontrol->attrvalue0;
      $returnData['attrtype1']    = $kontrol->attrtype1;
      $returnData['attrvalue1']   = $kontrol->attrvalue1;
      $returnData['attrtype2']    = $kontrol->attrtype2;
      $returnData['attrvalue2']   = $kontrol->attrvalue2;
      $returnData['attrtype3']    = $kontrol->attrtype3;
      $returnData['attrvalue3']   = $kontrol->attrvalue3;
      $returnData['attrtype4']    = $kontrol->attrtype4;
      $returnData['attrvalue4']   = $kontrol->attrvalue4;
      $returnData['attrtype5']    = $kontrol->attrtype5;
      $returnData['attrvalue5']   = $kontrol->attrvalue5;
      $returnData['attrtype6']    = $kontrol->attrtype6;
      $returnData['attrvalue6']   = $kontrol->attrvalue6;
      $returnData['status']       = $kontrol->status;
      $returnData['sell_count']   = $kontrol->sell_count;
      $returnData['id']           = $kontrol->id;
      echo json_encode($returnData);
      exit;
    }
  }

  public function Duzenle()
  {
    if (!IsAllowedViewModule('nesneMarketEsyaDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'category_id' => ['label' => lang('Genel.kategori'),  'rules' => "required|integer"],
      'vnum'        => ['label' => lang('Genel.esya'),      'rules' => "required|integer"],
      'item_name'   => ['label' => lang('Genel.esya'),      'rules' => "required"],
      'price'       => ['label' => lang('Genel.fiyat'),     'rules' => "required|integer"],
      'count'       => ['label' => lang('Genel.adet'),      'rules' => "required|integer"],
      'id'          => ['label' => lang('Genel.esya'),      'rules' => "required|integer"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->nesneMarketModel->Kontrol($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Esya.cikti.esyaYok'));
      }
      $kategoriKontrol  = $this->nesneMarketModel->KategoriKontrol($request->getPost('category_id'),$db);
      if (!$kategoriKontrol) {
        responseResult('error',lang('NesneMarket.cikti.kategoriYok'));
      }
      $esyaKontrol  = $this->nesneMarketModel->ItemProtoKontrol($request->getPost('vnum'),$db);
      if (!$esyaKontrol) {
        responseResult('error',lang('Esya.cikti.esyaYok'));
      }
      $data = [
        'category_id' =>  $kategoriKontrol->cat_id,
        'vnum'        =>  $esyaKontrol->vnum,
        'item_name'   =>  mb_convert_encoding($request->getPost('item_name'), 'ISO-8859-9' ,"UTF-8"),
        'price'       =>  $request->getPost('price'),
        'count'       =>  $request->getPost('count'),
        'time_type'   =>  $request->getPost('time_type'),
        'price_type'  =>  $request->getPost('price_type'),
        'socket0'     =>  $request->getPost('socket0'),
        'socket1'     =>  $request->getPost('socket1'),
        'socket2'     =>  $request->getPost('socket2'),
        'socket3'     =>  $request->getPost('socket3'),
        'attrtype0'   =>  $request->getPost('attrtype0'),
        'attrvalue0'  =>  $request->getPost('attrvalue0'),
        'attrtype1'   =>  $request->getPost('attrtype1'),
        'attrvalue1'  =>  $request->getPost('attrvalue1'),
        'attrtype2'   =>  $request->getPost('attrtype2'),
        'attrvalue2'  =>  $request->getPost('attrvalue2'),
        'attrtype3'   =>  $request->getPost('attrtype3'),
        'attrvalue3'  =>  $request->getPost('attrvalue3'),
        'attrtype4'   =>  $request->getPost('attrtype4'),
        'attrvalue4'  =>  $request->getPost('attrvalue4'),
        'attrtype5'   =>  $request->getPost('attrtype5'),
        'attrvalue5'  =>  $request->getPost('attrvalue5'),
        'attrtype6'   =>  $request->getPost('attrtype6'),
        'attrvalue6'  =>  $request->getPost('attrvalue6'),
        'status'      =>  $request->getPost('status'),
        'sell_count'  =>  $request->getPost('sell_count'),
      ];
      $result = $this->nesneMarketModel->Guncelle($data,$kontrol->id,$db);
      if ($result) {
        LogAdd(lang('NesneMarket.kayit.esyaDuzenlendi',[ 'category' => mb_convert_encoding($kontrol->cat_name, 'UTF-8' ,"ISO-8859-9"), 'name' => mb_convert_encoding($kontrol->item_name, 'UTF-8' ,"ISO-8859-9") ]),'NesneMarket/Index',session('user_id'));
        responseResult('success',lang('NesneMarket.cikti.esyaDuzenlendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Sil()
  {
    if (!IsAllowedViewModule('nesneMarketEsyaSilebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'id'  => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->nesneMarketModel->Kontrol($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Esya.sayfa.esyaYok'));
      }else {
        $result = $this->nesneMarketModel->Sil($kontrol->id,$db);
        if ($result) {
          LogAdd(lang('NesneMarket.kayit.esyaSilindi',[ 'category' => mb_convert_encoding($kontrol->cat_name, 'UTF-8' ,"ISO-8859-9"), 'name' => mb_convert_encoding($kontrol->item_name, 'UTF-8' ,"ISO-8859-9") ]),'NesneMarket/Index',session('user_id'));
          responseResult('success',lang('NesneMarket.cikti.esyaSilindi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function SunucuyaGonder()
  {
    if (!IsAllowedViewModule('nesneMarketKategoriEkleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    if (p2pStatus==0) {
      responseResult('error',lang('Genel.p2pKapali'));
    }
    foreach (p2pPorts as $key => $value) {
      SendServer('P',"RELOAD",$value);
    }
    LogAdd(lang('NesneMarket.cikti.sunucuyaGonderildi'),'NesneMarket/Index',session('user_id'));
    responseResult('success',lang('NesneMarket.cikti.sunucuyaGonderildi'));
  }
}
