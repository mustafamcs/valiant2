<ul class="nav nav-tabs">
  <?php if (IsAllowedViewModule('logoyuGuncelleyebilsin')): ?>
    <li class="nav-item">
      <a href="<?=base_url('Ayarlar/LogoYukle')?>" class="nav-link <?=WebTitle('LogoYukle')?'active':false?>">
        <svg xmlns="http://www.w3.org/2000/svg" class="icon me-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><line x1="15" y1="8" x2="15.01" y2="8" /><rect x="4" y="4" width="16" height="16" rx="3" /><path d="M4 15l4 -4a3 5 0 0 1 3 0l5 5" /><path d="M14 14l1 -1a3 5 0 0 1 3 0l2 2" /></svg>
        <?=lang('Ayarlar.sayfa.logoYukle')?>
      </a>
    </li>
  <?php endif; ?>
  <?php if (IsAllowedViewModule('faviconGuncelleyebilsin')): ?>
    <li class="nav-item">
      <a href="<?=base_url('Ayarlar/FaviconYukle')?>" class="nav-link <?=WebTitle('FaviconYukle')?'active':false?>">
        <svg xmlns="http://www.w3.org/2000/svg" class="icon me-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><line x1="15" y1="8" x2="15.01" y2="8" /><rect x="4" y="4" width="16" height="16" rx="3" /><path d="M4 15l4 -4a3 5 0 0 1 3 0l5 5" /><path d="M14 14l1 -1a3 5 0 0 1 3 0l2 2" /></svg>
        <?=lang('Ayarlar.sayfa.faviconYukle')?>
      </a>
    </li>
  <?php endif; ?>
  <?php if (IsAllowedViewModule('siteAyarlariniGuncelleyebilsin')): ?>
    <li class="nav-item">
      <a href="<?=base_url('Ayarlar/Site')?>" class="nav-link <?=WebTitle('Site')?'active':false?>">
        <svg xmlns="http://www.w3.org/2000/svg" class="icon me-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M10.325 4.317c.426 -1.756 2.924 -1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543 -.94 3.31 .826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756 .426 1.756 2.924 0 3.35a1.724 1.724 0 0 0 -1.066 2.573c.94 1.543 -.826 3.31 -2.37 2.37a1.724 1.724 0 0 0 -2.572 1.065c-.426 1.756 -2.924 1.756 -3.35 0a1.724 1.724 0 0 0 -2.573 -1.066c-1.543 .94 -3.31 -.826 -2.37 -2.37a1.724 1.724 0 0 0 -1.065 -2.572c-1.756 -.426 -1.756 -2.924 0 -3.35a1.724 1.724 0 0 0 1.066 -2.573c-.94 -1.543 .826 -3.31 2.37 -2.37c1 .608 2.296 .07 2.572 -1.065z" /><circle cx="12" cy="12" r="3" /></svg>
        <?=lang('Ayarlar.sayfa.siteAyarlari')?>
      </a>
    </li>
  <?php endif; ?>
  <?php if (IsAllowedViewModule('javascriptKodlariniGuncelleyebilsin')): ?>
    <li class="nav-item">
      <a href="<?=base_url('Ayarlar/Javascript')?>" class="nav-link <?=WebTitle('Javascript')?'active':false?>">
        <svg xmlns="http://www.w3.org/2000/svg" class="icon me-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><polyline points="7 8 3 12 7 16" /><polyline points="17 8 21 12 17 16" /><line x1="14" y1="4" x2="10" y2="20" /></svg>
        <?=lang('Ayarlar.sayfa.javascriptKodlari')?>
      </a>
    </li>
  <?php endif; ?>
  <?php if (IsAllowedViewModule('smtpAyarlariniGuncelleyebilsin')): ?>
    <li class="nav-item">
      <a href="<?=base_url('Ayarlar/SMTP')?>" class="nav-link <?=WebTitle('SMTP')?'active':false?>">
        <svg xmlns="http://www.w3.org/2000/svg" class="icon me-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><rect x="3" y="5" width="18" height="14" rx="2" /><polyline points="3 7 12 13 21 7" /></svg>
        <?=lang('Ayarlar.sayfa.smtpAyarlari')?>
      </a>
    </li>
  <?php endif; ?>
  <?php if (IsAllowedViewModule('p2pAyarlariGuncelleyebilsin')): ?>
    <li class="nav-item">
      <a href="<?=base_url('Ayarlar/P2P')?>" class="nav-link <?=WebTitle('P2P')?'active':false?>">
        <svg xmlns="http://www.w3.org/2000/svg" class="icon me-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M7 12l5 5l-1.5 1.5a3.536 3.536 0 1 1 -5 -5l1.5 -1.5z"></path><path d="M17 12l-5 -5l1.5 -1.5a3.536 3.536 0 1 1 5 5l-1.5 1.5z"></path><path d="M3 21l2.5 -2.5"></path><path d="M18.5 5.5l2.5 -2.5"></path><path d="M10 11l-2 2"></path><path d="M13 14l-2 2"></path></svg>
        <?=lang('Ayarlar.sayfa.p2pAyarlari')?>
      </a>
    </li>
  <?php endif; ?>
  <?php if (IsAllowedViewModule('ikonAyarlariGuncelleyebilsin')): ?>
    <li class="nav-item">
      <a href="<?=base_url('Ayarlar/Ikon')?>" class="nav-link <?=WebTitle('Ikon')?'active':false?>">
        <svg xmlns="http://www.w3.org/2000/svg" class="icon me-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><line x1="15" y1="8" x2="15.01" y2="8"></line><rect x="4" y="4" width="16" height="16" rx="3"></rect><path d="M4 15l4 -4a3 5 0 0 1 3 0l5 5"></path><path d="M14 14l1 -1a3 5 0 0 1 3 0l2 2"></path></svg>
        <?=lang('Ayarlar.sayfa.ikonAyarlari')?>
      </a>
    </li>
  <?php endif; ?>
</ul>
