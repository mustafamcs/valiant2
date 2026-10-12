<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class Yukseltme extends BaseController
{
  public $viewFolder      = "";
  public $yukseltmeModel  = "";

  public function __construct()
  {
    $this->viewFolder     = "Yukseltme";
    $this->yukseltmeModel = model('Yukseltme_model');
    if (!session('user_id')) {
      header('Location: '.base_url('GirisYap'));
      exit;
    }
  }

  public function Index()
  {
    if (!IsAllowedViewModule('yukseltmeGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $viewData['viewFolder'] = $this->viewFolder;
    $viewData = array_merge(ConstantHeader(),$viewData);
    return view("{$this->viewFolder}/Index",$viewData);
  }

  public function Ajax()
  {
    if (!IsAllowedViewModule('yukseltmeGorebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $db       = \Config\Database::connect('metin2');
    $request  = \Config\Services::request();
    $siralama = ['id','id','cost','prob'];
    if ($request->getPost('startID') && $request->getPost('finishID')) {
      $yaz = $this->yukseltmeModel->AjaxFiltrele($request->getPost('startID'),$request->getPost('finishID'),$request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }else{
      $yaz = $this->yukseltmeModel->Ajax($request->getPost('start'),$request->getPost('length'),$siralama[$request->getPost('order[0][column]')],$request->getPost('order[0][dir]'),$db);
    }
    $data = [];
    foreach ($yaz as $key => $value) {
      $sub_array = [];
      $sub_array[] = $value->id;
      $items = "";
      for ($i=0; $i < 5 ; $i++) {
        $vnum   = 'vnum'.$i;
        $count  = 'count'.$i;
        if ($value->$vnum>0 && $value->$count>0) {
          $itemIcon = $this->yukseltmeModel->ItemIcon($value->$vnum);
          if (!empty($itemIcon) && $itemIcon!="-") {
            $items .= '<img src="'.base_url('assets/img/icon/'.$itemIcon->icon).'" title="'.$value->$vnum.'"> x '.$value->$count.' - ';
          }else {
            $items .= $value->$vnum.' x '.$value->$count.' - ';
          }
        }
      }
      $sub_array[] = trim($items," - ");
      $sub_array[] = number_format($value->cost,0,'.','.');
      $sub_array[] = $value->prob;
      if (IsAllowedViewModule('yukseltmeDuzenleyebilsin') || IsAllowedViewModule('yukseltmeSilebilsin')) {
        $buttons = "";
        if (IsAllowedViewModule('yukseltmeDuzenleyebilsin')) {
          $buttons .= '<a class="btn btn-primary pt-1 pb-1 ps-2 pe-2" data-bs-toggle="modal" data-bs-target="#duzenle" href="javascript:void(0)" data-id="'.$value->id.'">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon m-0" style="width:25px;height:25px" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 7h-3a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-3" /><path d="M9 15h3l8.5 -8.5a1.5 1.5 0 0 0 -3 -3l-8.5 8.5v3" /><line x1="16" y1="5" x2="19" y2="8" /></svg>
          </a>';
        }
        if (IsAllowedViewModule('yukseltmeSilebilsin')) {
          $buttons .= '<a class="btn btn-danger pt-1 pb-1 ps-2 pe-2 ms-2 yukseltmeSil" href="javascript:void(0)" data-id="'.$value->id.'" data-header="'.lang('Genel.silBaslik').'" data-message="'.lang('Genel.buIslemGeriAlinamaz').'" data-yes="'.lang('Genel.evet').'" data-no="'.lang('Genel.hayir').'">
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

  public function Ekle()
  {
    if (!IsAllowedViewModule('yukseltmeEkleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'vnum0'       => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'count0'      => ['label' => lang('Genel.adet'),  'rules' => "required|integer"],
      'vnum1'       => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'count1'      => ['label' => lang('Genel.adet'),  'rules' => "required|integer"],
      'vnum2'       => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'count2'      => ['label' => lang('Genel.adet'),  'rules' => "required|integer"],
      'vnum3'       => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'count3'      => ['label' => lang('Genel.adet'),  'rules' => "required|integer"],
      'vnum4'       => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'count4'      => ['label' => lang('Genel.adet'),  'rules' => "required|integer"],
      'cost'        => ['label' => lang('Genel.fiyat'), 'rules' => "required|integer"],
      'prob'        => ['label' => lang('Genel.sans'),  'rules' => "required|integer"],
      'src_vnum'    => ['label' => 'src_vnum',          'rules' => "required|integer"],
      'result_vnum' => ['label' => 'result_vnum',       'rules' => "required|integer"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db   = \Config\Database::connect('metin2');
      $data = [
        'vnum0'       =>  $request->getPost('vnum0'),
        'count0'      =>  $request->getPost('count0'),
        'vnum1'       =>  $request->getPost('vnum1'),
        'count1'      =>  $request->getPost('count1'),
        'vnum2'       =>  $request->getPost('vnum2'),
        'count2'      =>  $request->getPost('count2'),
        'vnum3'       =>  $request->getPost('vnum3'),
        'count3'      =>  $request->getPost('count3'),
        'vnum4'       =>  $request->getPost('vnum4'),
        'count4'      =>  $request->getPost('count4'),
        'cost'        =>  $request->getPost('cost'),
        'prob'        =>  $request->getPost('prob'),
        'src_vnum'    =>  $request->getPost('src_vnum'),
        'result_vnum' =>  $request->getPost('result_vnum'),
      ];
      $result = $this->yukseltmeModel->Ekle($data,$db);
      if ($result) {
        LogAdd(lang('Yukseltme.kayit.yukseltmeEklendi'),'Yukseltme/Index',session('user_id'));
        responseResult('success',lang('Yukseltme.cikti.yukseltmeEklendi'));
      }else {
        responseResult('error',lang('Genel.bilinmeyenHata'));
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Detay($id=0)
  {
    if (!IsAllowedViewModule('yukseltmeDuzenleyebilsin')) {
      responseResult('error',lang('Genel.yetkinYok'));
    }
    $request  = \Config\Services::request();
    $db       = \Config\Database::connect('metin2');
    $kontrol  = $this->yukseltmeModel->Kontrol($id,$db);
    if (!$kontrol) {
      responseResult('error',lang('Yukseltme.cikti.yukseltmeYok'));
    }else {
      $returnData['id']           = $kontrol->id;
      $returnData['vnum0']        = $kontrol->vnum0;
      $returnData['count0']       = $kontrol->count0;
      $returnData['vnum1']        = $kontrol->vnum1;
      $returnData['count1']       = $kontrol->count1;
      $returnData['vnum2']        = $kontrol->vnum2;
      $returnData['count2']       = $kontrol->count2;
      $returnData['vnum3']        = $kontrol->vnum3;
      $returnData['count3']       = $kontrol->count3;
      $returnData['vnum4']        = $kontrol->vnum4;
      $returnData['count4']       = $kontrol->count4;
      $returnData['cost']         = $kontrol->cost;
      $returnData['prob']         = $kontrol->prob;
      $returnData['src_vnum']     = $kontrol->src_vnum;
      $returnData['result_vnum']  = $kontrol->result_vnum;
      echo json_encode($returnData);
      exit;
    }
  }

  public function Duzenle()
  {
    if (!IsAllowedViewModule('yukseltmeDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'vnum0'       => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'count0'      => ['label' => lang('Genel.adet'),  'rules' => "required|integer"],
      'vnum1'       => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'count1'      => ['label' => lang('Genel.adet'),  'rules' => "required|integer"],
      'vnum2'       => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'count2'      => ['label' => lang('Genel.adet'),  'rules' => "required|integer"],
      'vnum3'       => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'count3'      => ['label' => lang('Genel.adet'),  'rules' => "required|integer"],
      'vnum4'       => ['label' => lang('Genel.esya'),  'rules' => "required|integer"],
      'count4'      => ['label' => lang('Genel.adet'),  'rules' => "required|integer"],
      'cost'        => ['label' => lang('Genel.fiyat'), 'rules' => "required|integer"],
      'prob'        => ['label' => lang('Genel.sans'),  'rules' => "required|integer"],
      'src_vnum'    => ['label' => 'src_vnum',          'rules' => "required|integer"],
      'result_vnum' => ['label' => 'result_vnum',       'rules' => "required|integer"],
      'id'          => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->yukseltmeModel->Kontrol($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Yukseltme.cikti.yukseltmeYok'));
      }else {
        $data = [
          'vnum0'       =>  $request->getPost('vnum0'),
          'count0'      =>  $request->getPost('count0'),
          'vnum1'       =>  $request->getPost('vnum1'),
          'count1'      =>  $request->getPost('count1'),
          'vnum2'       =>  $request->getPost('vnum2'),
          'count2'      =>  $request->getPost('count2'),
          'vnum3'       =>  $request->getPost('vnum3'),
          'count3'      =>  $request->getPost('count3'),
          'vnum4'       =>  $request->getPost('vnum4'),
          'count4'      =>  $request->getPost('count4'),
          'cost'        =>  $request->getPost('cost'),
          'prob'        =>  $request->getPost('prob'),
          'src_vnum'    =>  $request->getPost('src_vnum'),
          'result_vnum' =>  $request->getPost('result_vnum'),
        ];
        $result = $this->yukseltmeModel->Guncelle($data,$kontrol->id,$db);
        if ($result) {
          LogAdd(lang('Yukseltme.kayit.yukseltmeDuzenlendi',['id' => $kontrol->id]),'Yukseltme/Index',session('user_id'));
          responseResult('success',lang('Yukseltme.cikti.yukseltmeDuzenlendi'));
        }else {
          responseResult('error',lang('Genel.bilinmeyenHata'));
        }
      }
    }else {
      responseResult('error',$validation->getErrors());
    }
  }

  public function Sil()
  {
    if (!IsAllowedViewModule('yukseltmeSilebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    $request    =  \Config\Services::request();
    $validation =  \Config\Services::validation();
    $validation->setRules([
      'id'  => ['rules' => "required"],
    ]);
    if ($validation->withRequest($this->request)->run()){
      $db       = \Config\Database::connect('metin2');
      $kontrol  = $this->yukseltmeModel->Kontrol($request->getPost('id'),$db);
      if (!$kontrol) {
        responseResult('error',lang('Yukseltme.cikti.yukseltmeYok'));
      }else {
        $result = $this->yukseltmeModel->Sil($kontrol->id,$db);
        if ($result) {
          LogAdd(lang('Yukseltme.kayit.yukseltmeSilindi',['id' => $kontrol->id]),'Yukseltme/Index',session('user_id'));
          responseResult('success',lang('Yukseltme.cikti.yukseltmeSilindi'));
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
    if (!IsAllowedViewModule('yukseltmeEkleyebilsin') && !IsAllowedViewModule('yukseltmeDuzenleyebilsin')) {
      return redirect()->to(base_url('YetkisizErisim'));
    }
    if (p2pStatus==0) {
      responseResult('error',lang('Genel.p2pKapali'));
    }
    foreach (p2pPorts as $key => $value) {
      SendServer('P',"RELOAD",$value);
    }
    LogAdd(lang('Yukseltme.cikti.sunucuyaGonderildi'),'Yukseltme/Index',session('user_id'));
    responseResult('success',lang('Yukseltme.cikti.sunucuyaGonderildi'));
  }
}
