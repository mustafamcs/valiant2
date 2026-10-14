<?php
$__envFile = dirname(__DIR__, 4) . DIRECTORY_SEPARATOR . '.env';
$__env = [];
if (is_readable($__envFile)) {
	foreach (file($__envFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $__line) {
		$__line = ltrim(trim($__line), "\xEF\xBB\xBF");
		if ($__line === '' || $__line[0] === '#' || !str_contains($__line, '=')) {
			continue;
		}
		[$__k, $__v] = explode('=', $__line, 2);
		$__env[ltrim(trim($__k), "\xEF\xBB\xBF")] = trim($__v, " \t\"'");
	}
}
$__get = static function (string $key, string $default = '') use ($__env): string {
	return $__env[$key] ?? $default;
};

$__channelPorts = array_values(array_filter(array_map('trim', explode(',', $__get('PANEL_P2P_PORTS', '30003,30005,30007,30009')))));
$__statPorts = array_values(array_filter(array_map('trim', explode(',', $__get('PANEL_P2P_CHANNEL_PORTS', '30003,30005,30007,30009')))));

define('p2pStatus',      1);
define('p2pHost',        $__get('ADMINPAGE_IP', '127.0.0.1'));
define('p2pPassword',    $__get('ADMINPAGE_PASSWORD'));
define('p2pPorts',       $__channelPorts);
define('p2pStatistics',  1);
define('p2pChannel',     $__statPorts);

unset($__envFile, $__env, $__get, $__channelPorts, $__statPorts);
