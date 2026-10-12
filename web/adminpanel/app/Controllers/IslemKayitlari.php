<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class IslemKayitlari extends BaseController
{
  public $viewFolder      = "";
  public $islemKayitModel = "";

  public function __construct()
  {
    $this->viewFolder       = "IslemKayitlari";
    $this->islemKayitModel  = model('Islem_kayit_model');
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function Index()
  {
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Index",$viewData);
  }

  public function Ajax()
  {
    $db       = \Config\Database::connect();
    $request  = \Config\Services::request();
    if (IsAllowedViewModule('tumBildirimleriGorebilsin')) {
      $siralama = ['log_id','log_user_id','log_content','log_link','log_status','log_date','log_ip'];
    } else {
      $siralama = ['log_id','log_content','log_link','log_status','log_date','log_ip'];
    }
    if ($request->getPost('search[value]')) {
      if ($request->getPost('log_status')=="" && $request->getPost('log_user_id')=="" && IsAllowedViewModule('tumBildirimleriGorebilsin')) {
        $yaz = $this->islemKayitModel->AjaxAraHepsi($request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }else if ($request->getPost('log_status')!="" && $request->getPost('log_user_id')!="" && IsAllowedViewModule('tumBildirimleriGorebilsin')) {
        $yaz = $this->islemKayitModel->AjaxAraFiltreleDurumKullanici($request->getPost('log_status'),$request->getPost('log_user_id'),$request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }else if ($request->getPost('log_status')!="" && $request->getPost('log_user_id')=="" && IsAllowedViewModule('tumBildirimleriGorebilsin')) {
        $yaz = $this->islemKayitModel->AjaxAraFiltreleDurumHepsi($request->getPost('log_status'),$request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }else if ($request->getPost('log_user_id')!="" && IsAllowedViewModule('tumBildirimleriGorebilsin')) {
        $yaz = $this->islemKayitModel->AjaxAraFiltreleKullanici($request->getPost('log_user_id'),$request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }else if ($request->getPost('log_status')!="") {
        $yaz = $this->islemKayitModel->AjaxAraFiltreleDurum($request->getPost('log_status'),$request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }else {
        $yaz = $this->islemKayitModel->AjaxAra($request->getPost('search[value]'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }
    }else{
      if ($request->getPost('log_status')=="" && $request->getPost('log_user_id')=="" && IsAllowedViewModule('tumBildirimleriGorebilsin')) {
        $yaz = $this->islemKayitModel->AjaxHepsi($request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }else if ($request->getPost('log_status')!="" && $request->getPost('log_user_id')!="" && IsAllowedViewModule('tumBildirimleriGorebilsin')) {
        $yaz = $this->islemKayitModel->AjaxFiltreleDurumKullanici($request->getPost('log_status'),$request->getPost('log_user_id'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }else if ($request->getPost('log_status')!="" && $request->getPost('log_user_id')=="" && IsAllowedViewModule('tumBildirimleriGorebilsin')) {
        $yaz = $this->islemKayitModel->AjaxFiltreleDurumHepsi($request->getPost('log_status'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }else if ($request->getPost('log_user_id')!="" && IsAllowedViewModule('tumBildirimleriGorebilsin')) {
        $yaz = $this->islemKayitModel->AjaxFiltreleKullanici($request->getPost('log_user_id'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }else if ($request->getPost('log_status')!="") {
        $yaz = $this->islemKayitModel->AjaxFiltreleDurum($request->getPost('log_status'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }else {
        $yaz = $this->islemKayitModel->Ajax($request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
      }
    }
    $data = [];
    if (IsAllowedViewModule('tumBildirimleriGorebilsin')) {
      foreach ($yaz as $key => $value) {
        $sub_array = [];
        $sub_array[] = $value->log_id;
        $sub_array[] = '<a target="_blank" class="text-muted" href="'.base_url('Kullanicilar/Detay/'.$value->user_id).'">'.$value->user_name.'</a>';
        $sub_array[] = strip_tags($value->log_content);
        $sub_array[] = '<a target="_blank" class="text-muted" href="'.base_url($value->log_link).'">'.base_url($value->log_link).'</a>';
        $sub_array[] = ($value->log_status=="0"?lang('Genel.gorulmedi'):lang('Genel.goruldu'));
        $sub_array[] = DateDMYHM($value->log_date);
        $sub_array[] = $value->log_ip;
        $data[] = $sub_array;
      }
    }else {
      foreach ($yaz as $key => $value) {
        $sub_array = [];
        $sub_array[] = $value->log_id;
        $sub_array[] = strip_tags($value->log_content);
        $sub_array[] = '<a target="_blank" class="text-muted" href="'.base_url($value->log_link).'">'.base_url($value->log_link).'</a>';
        $sub_array[] = ($value->log_status=="0"?lang('Genel.gorulmedi'):lang('Genel.goruldu'));
        $sub_array[] = DateDMYHM($value->log_date);
        $sub_array[] = $value->log_ip;
        $data[] = $sub_array;
      }
    }
    $output = array(
      "draw"            =>  intval($_POST["draw"]),
      "recordsFiltered" =>  (count($yaz)==$request->getPost('length')?$request->getPost('start')+$request->getPost('length')+1:0),
      "data"            =>  $data
    );
    echo json_encode($output, JSON_INVALID_UTF8_SUBSTITUTE);
    exit;
  }

  public function Kullanicilar()
  {
    if (IsAllowedViewModule('tumBildirimleriGorebilsin')) {
      $request    = \Config\Services::request();
      $search = $request->getGet('q');
      if (!$search) {
        $search = "";
      }
      $kullanicilar = $this->islemKayitModel->Kullanicilar($search);
      $data[] = [
        'id'    => "",
        'text'  => lang('Genel.hepsi')
      ];
      foreach ($kullanicilar as $key => $value) {
        $data[] = [
          'id'    => $value->user_id,
          'text'  => $value->user_name
        ];
      }
      echo json_encode($data);
      exit;
    }
  }

  public function IslemKayitiSayisi()
  {
    $gorulmemisIslemKayitiSayisi = $this->islemKayitModel->GorulmemisIslemKayitiSayisi();
    $response['islemKayitiSayisi'] = $gorulmemisIslemKayitiSayisi;
    echo json_encode($response);
    exit;
  }

  public function SonIslemKayitlari()
  {
    helper('text');
    $sonIslemKayitlari = $this->islemKayitModel->SonIslemKayitlari();
    $response['sonIslemKayitlari'] = null;
    if (!empty($sonIslemKayitlari)) {
      foreach ($sonIslemKayitlari as $key => $value) {
        $response['sonIslemKayitlari'][] = [
          'text' => character_limiter($value->log_content,75),
          'link' => base_url($value->log_link),
          'time' => DateDMYHM($value->log_date),
        ];
      }
      $this->islemKayitModel->HepsiniOku();
    }
    echo json_encode($response);
    exit;
  }
}
