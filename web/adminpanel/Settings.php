<?php
// Load secrets and connection settings from the project root .env file.
$__envFile = dirname(__DIR__, 2) . DIRECTORY_SEPARATOR . '.env';
$__env = [];
if (is_readable($__envFile)) {
	foreach (file($__envFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $__line) {
		$__line = trim($__line);
		if ($__line === '' || $__line[0] === '#' || !str_contains($__line, '=')) {
			continue;
		}
		[$__k, $__v] = explode('=', $__line, 2);
		$__env[trim($__k)] = trim($__v, " \t\"'");
	}
}
$__get = static function (string $key, string $default = '') use ($__env): string {
	return $__env[$key] ?? $default;
};

define('SiteUrl',         $__get('PANEL_BASE_URL', 'http://localhost:8090/')); //Site Url
define('SqlHost',         $__get('MYSQL_HOST', '127.0.0.1')); // panel veritabani host
define('SqlTable',        $__get('PANEL_DB_DATABASE', 'valiant_panel')); // panel veritabani adi
define('SqlUser',         $__get('PANEL_DB_USER', 'valiant_panel')); // panel kullanici adi
define('SqlPassword',     $__get('PANEL_DB_PASSWORD')); // panel kullanici sifresi
define('Metin2Host',      $__get('MYSQL_HOST', '127.0.0.1')); // oyun veritabani host
define('Metin2User',      $__get('MYSQL_USER')); // oyun veritabani kullanici
define('Metin2Password',  $__get('MYSQL_PASSWORD')); // oyun veritabani sifre
define('ENVIRONMENT',     'development'); // development ve ya production
define('versionKey',      'v1.02'); // versiyon sabiti

unset($__envFile, $__env, $__get);
