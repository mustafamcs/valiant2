<?php

namespace Config;

use CodeIgniter\Config\BaseConfig;
use CodeIgniter\Filters\CSRF;
use CodeIgniter\Filters\DebugToolbar;
// use CodeIgniter\Filters\Honeypot;

class Filters extends BaseConfig
{
	/**
	* Configures aliases for Filter classes to
	* make reading things nicer and simpler.
	*
	* @var array
	*/
	public $aliases = [
		'csrf'     => CSRF::class,
		'toolbar'  => DebugToolbar::class,
		// 'honeypot' => Honeypot::class,
	];

	/**
	* List of filter aliases that are always
	* applied before and after every request.
	*
	* @var array
	*/
	public $globals = [
		'before' => [
			// 'honeypot',
			'csrf'	=>	[
				'except' => [
					'IslemKayitlari/Ajax',
					'Kullanicilar/Ajax',
					'Kullanicilar/Durum',
					'Kullanicilar/OturumuSonlandir',
					'Kullanicilar/IslemKayitlariAjax/[0-9]+',
					'GM/Ajax',
					'GM/Sil',
					'Efsun/Ajax',
					'Efsun/NadirAjax',
					'Yukseltme/Ajax',
					'Yukseltme/Sil',
					'VeriIslemleri/AjaxID',
					'VeriIslemleri/SilID',
					'VeriIslemleri/AjaxText',
					'VeriIslemleri/SilText',
					'VeriIslemleri/AjaxHarita',
					'VeriIslemleri/SilHarita',
					'Esya/Ajax',
					'Esya/Droplar/[0-9]+',
					'Esya/DropEkle',
					'Esya/DropGuncelle',
					'Esya/DropSil',
					'Esya/AjaxAra',
					'Oyuncu/AjaxNesneMarket/[0-9]+',
					'Canavar/Ajax',
					'Canavar/Droplar/[0-9]+',
					'Canavar/DropEkle',
					'Canavar/DropGuncelle',
					'Canavar/DropSil',
					'Canavar/DropLevel/[0-9]+',
					'Canavar/DropLevelEkle',
					'Canavar/DropLevelGuncelle',
					'Canavar/DropLevelSil',
					'Canavar/DropKill/[0-9]+',
					'Canavar/DropKillEkle',
					'Canavar/DropKillGuncelle',
					'Canavar/DropKillSil',
					'Kayitlar/AjaxBoot',
					'Kayitlar/AjaxGM',
					'Kayitlar/AjaxNesneMarket',
					'Kayitlar/AjaxLevel',
					'Kayitlar/AjaxPazar',
					'Oyuncu/AjaxKarakterNesneMarket/[0-9]+',
					'Oyuncu/AjaxKarakterPazar/[0-9]+',
					'Oyuncu/AjaxKarakterGenel/[0-9]+',
					'Balikcilik/Ajax',
					'Balikcilik/Sil',
					'Cark/Ajax',
					'Cark/Sil',
					'Biyolog/Ajax',
					'Biyolog/Sil',
					'Patch/Ajax',
					'Patch/Sil',
					'Sandik/Ajax',
					'Sandik/ItemSil',
					'Sandik/ItemDuzenle',
					'Sandik/Sil',
					'NesneMarket/KategoriAjax',
					'NesneMarket/KategoriSil',
					'NesneMarket/Ajax',
					'NesneMarket/Durum',
					'NesneMarket/Sil',
					'NPC/Ajax',
					'NPC/Sil',
					'NPC/Esyalar/[0-9]+',
					'NPC/EsyaEkle',
					'NPC/EsyaGuncelle',
					'NPC/EsyaSil',
					'Harita/DetayAjax',
					'Harita/KaydetAjax',
					'Harita/IzgaraDagitAjax',
					'Arindirma/EkleAjax',
					'Arindirma/SilAjax',
					'Ekonomi/KaynakAnalizAjax',
					'Ekonomi/DiscordWebhookAjax',
					'Sistemler/BayrakDegistirAjax',
					'Sistemler/ProfilUygulaAjax',
					'Sistemler/BaslangicKaydetAjax',
				]
			],
		],
		'after'  => [
			'toolbar',
			// 'honeypot',
		],
	];

	/**
	* List of filter aliases that works on a
	* particular HTTP method (GET, POST, etc.).
	*
	* Example:
	* 'post' => ['csrf', 'throttle']
	*
	* @var array
	*/
	public $methods = [];

	/**
	* List of filter aliases that should run on any
	* before or after URI patterns.
	*
	* Example:
	* 'isLoggedIn' => ['before' => ['account/*', 'profiles/*']]
	*
	* @var array
	*/
	public $filters = [];
}
