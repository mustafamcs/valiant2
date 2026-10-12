<?php

namespace App\Controllers;
use App\Controllers\BaseController;

class Yonlendir extends BaseController
{
  public function Index()
  {
    $this->response->setStatusCode(404);
    header('Location: '.base_url('Hata'));
    exit;
  }

  public function Hata($type="")
  {
    $this->response->setStatusCode(404);
    $refererLink = \Config\Services::request()->getUserAgent()->getReferrer();
    if (!empty($refererLink)) {
      $viewData['link'] = $refererLink;
    }else {
      $viewData['link'] = base_url();
    }
    return view("Hata/Error_404",$viewData);
  }

  public function YetkisizErisim($type="")
  {
    $this->response->setStatusCode(403);
    $refererLink = \Config\Services::request()->getUserAgent()->getReferrer();
    if (!empty($refererLink)) {
      $viewData['link'] = $refererLink;
    }else {
      $viewData['link'] = base_url();
    }
    return view("Hata/Error_403",$viewData);
  }
}
