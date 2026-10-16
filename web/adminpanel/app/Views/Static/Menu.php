<div class="navbar-expand-md">
  <div class="collapse navbar-collapse" id="navbar-menu">
    <div class="navbar navbar-light">
      <div class="container-xl">
        <ul class="navbar-nav">
          <li class="nav-item <?=WebTitle('Anasayfa')?'active':false?>">
            <a class="nav-link" href="<?=base_url('Anasayfa/Index')?>" >
              <span class="nav-link-icon d-inline-block">
                <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><polyline points="5 12 3 12 12 3 21 12 19 12" /><path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-7" /><path d="M9 21v-6a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v6" /></svg>
              </span>
              <span class="nav-link-title">
                <?=lang('Anasayfa.sayfa.anasayfa')?>
              </span>
            </a>
          </li>
          <?php if (
            IsAllowedViewModule('esyaGorebilsin')
            || IsAllowedViewModule('esyaArayabilsin')
            ): ?>
            <li class="nav-item dropdown <?=WebTitle('Esya')?'active':false?>">
              <a class="nav-link dropdown-toggle" href="javascript:void(0)" data-bs-toggle="dropdown" role="button" aria-expanded="false" >
                <span class="nav-link-icon d-inline-block">
                  <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M4 4h6v6h-6z"></path><path d="M14 4h6v6h-6z"></path><path d="M4 14h6v6h-6z"></path><circle cx="17" cy="17" r="3"></circle></svg>
                </span>
                <span class="nav-link-title">
                  <?=lang('Esya.sayfa.esyaYonetimi')?>
                </span>
              </a>
              <div class="dropdown-menu">
                <?php if (IsAllowedViewModule('esyaGorebilsin')): ?>
                  <a class="dropdown-item" href="<?=base_url('Esya/Index')?>" >
                    <?=lang('Esya.sayfa.esyalar')?>
                  </a>
                <?php endif; ?>
                <?php if (IsAllowedViewModule('esyaArayabilsin')): ?>
                  <a class="dropdown-item" href="<?=base_url('Esya/Ara')?>" >
                    <?=lang('Esya.sayfa.ara')?>
                  </a>
                <?php endif; ?>
              </div>
            </li>
          <?php endif; ?>
          <?php if (IsAllowedViewModule('canavarGorebilsin')): ?>
            <li class="nav-item <?=WebTitle('Canavar')?'active':false?>">
              <a class="nav-link" href="<?=base_url('Canavar/Index')?>" >
                <span class="nav-link-icon d-inline-block">
                  <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"> <path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M14 4h6v6h-6z"></path><path d="M4 14h6v6h-6z"></path><circle cx="17" cy="17" r="3"></circle><circle cx="7" cy="7" r="3"></circle></svg>
                </span>
                <span class="nav-link-title">
                  <?=lang('Canavar.sayfa.canavarlar')?>
                </span>
              </a>
            </li>
          <?php endif; ?>
          <?php if (
            IsAllowedViewModule('bootKayitGorebilsin')
            || IsAllowedViewModule('gmKomutKayitGorebilsin')
            || IsAllowedViewModule('nesneKayitlariGorebilsin')
            || IsAllowedViewModule('levelKayitlariGorebilsin')
            || IsAllowedViewModule('pazarKayitlariGorebilsin')
            ): ?>
            <li class="nav-item dropdown <?=WebTitle('Kayitlar')?'active':false?>">
              <a class="nav-link dropdown-toggle" href="javascript:void(0)" data-bs-toggle="dropdown" role="button" aria-expanded="false" >
                <span class="nav-link-icon d-inline-block">
                  <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M9 5h-2a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-12a2 2 0 0 0 -2 -2h-2"></path><rect x="9" y="3" width="6" height="4" rx="2"></rect><path d="M9 12h6"></path><path d="M9 16h6"></path></svg>
                </span>
                <span class="nav-link-title">
                  <?=lang('Kayitlar.sayfa.kayitlar')?>
                </span>
              </a>
              <div class="dropdown-menu">
                <?php if (IsAllowedViewModule('bootKayitGorebilsin')): ?>
                  <a class="dropdown-item" href="<?=base_url('Kayitlar/Boot')?>" >
                    <?=lang('Kayitlar.sayfa.bootKayitlari')?>
                  </a>
                <?php endif; ?>
                <?php if (IsAllowedViewModule('gmKomutKayitGorebilsin')): ?>
                  <a class="dropdown-item" href="<?=base_url('Kayitlar/GM')?>" >
                    <?=lang('Kayitlar.sayfa.gmKomutKayitlari')?>
                  </a>
                <?php endif; ?>
                <?php if (IsAllowedViewModule('nesneKayitlariGorebilsin')): ?>
                  <a class="dropdown-item" href="<?=base_url('Kayitlar/NesneMarket')?>" >
                    <?=lang('Kayitlar.sayfa.nesneMarketKayitlari')?>
                  </a>
                <?php endif; ?>
                <?php if (IsAllowedViewModule('levelKayitlariGorebilsin')): ?>
                  <a class="dropdown-item" href="<?=base_url('Kayitlar/Level')?>" >
                    <?=lang('Kayitlar.sayfa.levelKayitlari')?>
                  </a>
                <?php endif; ?>
                <?php if (IsAllowedViewModule('pazarKayitlariGorebilsin')): ?>
                  <a class="dropdown-item" href="<?=base_url('Kayitlar/Pazar')?>" >
                    <?=lang('Kayitlar.sayfa.pazarKayitlari')?>
                  </a>
                <?php endif; ?>
              </div>
            </li>
          <?php endif; ?>

          <?php if (
            IsAllowedViewModule('gmGorebilsin')
            || IsAllowedViewModule('efsunlariGorebilsin')
            || IsAllowedViewModule('nadirEfsunlariGorebilsin')
            || IsAllowedViewModule('yukseltmeGorebilsin')
            || IsAllowedViewModule('balikcilikGorebilsin')
            || IsAllowedViewModule('carkGorebilsin')
            || IsAllowedViewModule('biyologGorebilsin')
            || IsAllowedViewModule('npcGorebilsin')
            || IsAllowedViewModule('sandikGorebilsin')
            ): ?>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="javascript:void(0)" data-bs-toggle="dropdown" role="button" aria-expanded="false" >
                <span class="nav-link-icon d-inline-block">
                  <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="7" cy="17" r="1"></circle><circle cx="12" cy="12" r="1"></circle><circle cx="17" cy="7" r="1"></circle></svg>
                </span>
                <span class="nav-link-title">
                  <?=lang('Anasayfa.sayfa.oyunIslemleri')?>
                </span>
              </a>
              <div class="dropdown-menu">
                <?php if (IsAllowedViewModule('gmGorebilsin')): ?>
                  <a class="dropdown-item" href="<?=base_url('GM/Index')?>" >
                    <span class="nav-link-icon d-inline-block">
                      <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><circle cx="9" cy="7" r="4" /><path d="M3 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2" /><path d="M16 3.13a4 4 0 0 1 0 7.75" /><path d="M21 21v-2a4 4 0 0 0 -3 -3.85" /></svg>
                    </span>
                    <span class="nav-link-title">
                      <?=lang('GM.sayfa.gm')?>
                    </span>
                  </a>
                <?php endif; ?>
                <?php if (
                  IsAllowedViewModule('efsunlariGorebilsin')
                  || IsAllowedViewModule('nadirEfsunlariGorebilsin')
                  ): ?>
                  <div class="dropend">
                    <a class="dropdown-item dropdown-toggle" href="#efsun" data-bs-toggle="dropdown" data-bs-auto-close="outside" role="button" aria-expanded="false" >
                      <svg xmlns="http://www.w3.org/2000/svg" class="icon me-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="14" cy="6" r="2"></circle><line x1="4" y1="6" x2="12" y2="6"></line><line x1="16" y1="6" x2="20" y2="6"></line><circle cx="8" cy="12" r="2"></circle><line x1="4" y1="12" x2="6" y2="12"></line><line x1="10" y1="12" x2="20" y2="12"></line><circle cx="17" cy="18" r="2"></circle><line x1="4" y1="18" x2="15" y2="18"></line><line x1="19" y1="18" x2="20" y2="18"></line></svg>
                      <?=lang('Efsun.sayfa.efsun')?>
                    </a>
                    <div class="dropdown-menu">
                      <?php if (IsAllowedViewModule('efsunlariGorebilsin')): ?>
                        <a class="dropdown-item" href="<?=base_url('Efsun/Index')?>" >
                          <?=lang('Efsun.sayfa.efsunAyarlari')?>
                        </a>
                      <?php endif; ?>
                      <?php if (IsAllowedViewModule('nadirEfsunlariGorebilsin')): ?>
                        <a class="dropdown-item" href="<?=base_url('Efsun/Nadir')?>" >
                          <?=lang('Efsun.sayfa.nadirEfsunAyarlari')?>
                        </a>
                      <?php endif; ?>
                    </div>
                  </div>
                <?php endif; ?>
                <?php if (IsAllowedViewModule('yukseltmeGorebilsin')): ?>
                  <a class="dropdown-item" href="<?=base_url('Yukseltme/Index')?>" >
                    <span class="nav-link-icon d-inline-block">
                      <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><rect x="4" y="4" width="16" height="16" rx="2"></rect><line x1="9" y1="12" x2="15" y2="12"></line><line x1="12" y1="9" x2="12" y2="15"></line></svg>
                    </span>
                    <span class="nav-link-title">
                      <?=lang('Yukseltme.sayfa.yukseltme')?>
                    </span>
                  </a>
                <?php endif; ?>
                <?php if (IsAllowedViewModule('balikcilikGorebilsin')): ?>
                  <a class="dropdown-item" href="<?=base_url('Balikcilik/Index')?>" >
                    <span class="nav-link-icon d-inline-block">
                      <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M10.325 4.317c.426 -1.756 2.924 -1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543 -.94 3.31 .826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756 .426 1.756 2.924 0 3.35a1.724 1.724 0 0 0 -1.066 2.573c.94 1.543 -.826 3.31 -2.37 2.37a1.724 1.724 0 0 0 -2.572 1.065c-.426 1.756 -2.924 1.756 -3.35 0a1.724 1.724 0 0 0 -2.573 -1.066c-1.543 .94 -3.31 -.826 -2.37 -2.37a1.724 1.724 0 0 0 -1.065 -2.572c-1.756 -.426 -1.756 -2.924 0 -3.35a1.724 1.724 0 0 0 1.066 -2.573c-.94 -1.543 .826 -3.31 2.37 -2.37c1 .608 2.296 .07 2.572 -1.065z" /><circle cx="12" cy="12" r="3" /></svg>
                    </span>
                    <span class="nav-link-title">
                      <?=lang('Balikcilik.sayfa.balikcilik')?>
                    </span>
                  </a>
                <?php endif; ?>
                <?php if (IsAllowedViewModule('carkGorebilsin')): ?>
                  <a class="dropdown-item" href="<?=base_url('Cark/Index')?>" >
                    <span class="nav-link-icon d-inline-block">
                      <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M10.325 4.317c.426 -1.756 2.924 -1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543 -.94 3.31 .826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756 .426 1.756 2.924 0 3.35a1.724 1.724 0 0 0 -1.066 2.573c.94 1.543 -.826 3.31 -2.37 2.37a1.724 1.724 0 0 0 -2.572 1.065c-.426 1.756 -2.924 1.756 -3.35 0a1.724 1.724 0 0 0 -2.573 -1.066c-1.543 .94 -3.31 -.826 -2.37 -2.37a1.724 1.724 0 0 0 -1.065 -2.572c-1.756 -.426 -1.756 -2.924 0 -3.35a1.724 1.724 0 0 0 1.066 -2.573c-.94 -1.543 .826 -3.31 2.37 -2.37c1 .608 2.296 .07 2.572 -1.065z" /><circle cx="12" cy="12" r="3" /></svg>
                    </span>
                    <span class="nav-link-title">
                      <?=lang('Cark.sayfa.cark')?>
                    </span>
                  </a>
                <?php endif; ?>
                <?php if (IsAllowedViewModule('biyologGorebilsin')): ?>
                  <a class="dropdown-item" href="<?=base_url('Biyolog/Index')?>" >
                    <span class="nav-link-icon d-inline-block">
                      <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M10.325 4.317c.426 -1.756 2.924 -1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543 -.94 3.31 .826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756 .426 1.756 2.924 0 3.35a1.724 1.724 0 0 0 -1.066 2.573c.94 1.543 -.826 3.31 -2.37 2.37a1.724 1.724 0 0 0 -2.572 1.065c-.426 1.756 -2.924 1.756 -3.35 0a1.724 1.724 0 0 0 -2.573 -1.066c-1.543 .94 -3.31 -.826 -2.37 -2.37a1.724 1.724 0 0 0 -1.065 -2.572c-1.756 -.426 -1.756 -2.924 0 -3.35a1.724 1.724 0 0 0 1.066 -2.573c-.94 -1.543 .826 -3.31 2.37 -2.37c1 .608 2.296 .07 2.572 -1.065z" /><circle cx="12" cy="12" r="3" /></svg>
                    </span>
                    <span class="nav-link-title">
                      <?=lang('Biyolog.sayfa.biyolog')?>
                    </span>
                  </a>
                <?php endif; ?>
                <?php if (IsAllowedViewModule('npcGorebilsin')): ?>
                  <a class="dropdown-item" href="<?=base_url('NPC/Index')?>" >
                    <span class="nav-link-icon d-inline-block">
                      <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M10.325 4.317c.426 -1.756 2.924 -1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543 -.94 3.31 .826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756 .426 1.756 2.924 0 3.35a1.724 1.724 0 0 0 -1.066 2.573c.94 1.543 -.826 3.31 -2.37 2.37a1.724 1.724 0 0 0 -2.572 1.065c-.426 1.756 -2.924 1.756 -3.35 0a1.724 1.724 0 0 0 -2.573 -1.066c-1.543 .94 -3.31 -.826 -2.37 -2.37a1.724 1.724 0 0 0 -1.065 -2.572c-1.756 -.426 -1.756 -2.924 0 -3.35a1.724 1.724 0 0 0 1.066 -2.573c-.94 -1.543 .826 -3.31 2.37 -2.37c1 .608 2.296 .07 2.572 -1.065z" /><circle cx="12" cy="12" r="3" /></svg>
                    </span>
                    <span class="nav-link-title">
                      <?=lang('NPC.sayfa.npc')?>
                    </span>
                  </a>
                <?php endif; ?>
                <?php if (IsAllowedViewModule('patchGorebilsin')): ?>
                  <a class="dropdown-item" href="<?=base_url('Patch/Index')?>" >
                    <span class="nav-link-icon d-inline-block">
                      <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2 -2v-2" /><path d="M7 9l5 -5l5 5" /><path d="M12 4l0 12" /></svg>
                    </span>
                    <span class="nav-link-title">
                      <?=lang('Patch.sayfa.patch')?>
                    </span>
                  </a>
                <?php endif; ?>
                <?php if (IsAllowedViewModule('sandikGorebilsin')): ?>
                  <a class="dropdown-item" href="<?=base_url('Sandik/Index')?>" >
                    <span class="nav-link-icon d-inline-block">
                      <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><rect x="3" y="8" width="18" height="4" rx="1" /><path d="M12 8v13" /><path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-7" /><path d="M7.5 8a2.5 2.5 0 0 1 0 -5a4.8 8 0 0 1 4.5 5a4.8 8 0 0 1 4.5 -5a2.5 2.5 0 0 1 0 5" /></svg>
                    </span>
                    <span class="nav-link-title">
                      <?=lang('Sandik.sayfa.sandik')?>
                    </span>
                  </a>
                <?php endif; ?>
                <div class="dropdown-divider"></div>
                <a class="dropdown-item" href="<?=base_url('Harita/Index')?>">
                  <span class="nav-link-icon d-inline-block">🗺️</span>
                  <span class="nav-link-title">Harita, Regen & Atlas Stüdyosu</span>
                </a>
                <a class="dropdown-item" href="<?=base_url('Arindirma/Index')?>">
                  <span class="nav-link-icon d-inline-block">⚗️</span>
                  <span class="nav-link-title">Arındırma (Cube) Editörü</span>
                </a>
                <a class="dropdown-item" href="<?=base_url('Ekonomi/Index')?>">
                  <span class="nav-link-icon d-inline-block">📊</span>
                  <span class="nav-link-title">Ekonomi, 360° Kaynak & Anti-Cheat</span>
                </a>
                <a class="dropdown-item" href="<?=base_url('Sistemler/Index')?>">
                  <span class="nav-link-icon d-inline-block">⚙️</span>
                  <span class="nav-link-title">Oyun Sistemleri (`Controls.h`) & Profiller</span>
                </a>
              </div>
            </li>
          <?php endif; ?>

          <?php if (
            IsAllowedViewModule('nesneMarketEsyaGorebilsin')
            || IsAllowedViewModule('nesneMarketKategoriGorebilsin')
            ): ?>
            <li class="nav-item dropdown <?=WebTitle('NesneMarket')?'active':false?>">
              <a class="nav-link dropdown-toggle" href="javascript:void(0)" data-bs-toggle="dropdown" role="button" aria-expanded="false" >
                <span class="nav-link-icon d-inline-block">
                  <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-shopping-cart" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="6" cy="19" r="2"></circle><circle cx="17" cy="19" r="2"></circle><path d="M17 17h-11v-14h-2"></path><path d="M6 5l14 1l-1 7h-13"></path></svg>
                </span>
                <span class="nav-link-title">
                  <?=lang('NesneMarket.sayfa.nesneMarket')?>
                </span>
              </a>
              <div class="dropdown-menu">
                <?php if (IsAllowedViewModule('nesneMarketEsyaGorebilsin')): ?>
                  <a class="dropdown-item" href="<?=base_url('NesneMarket/Index')?>" >
                    <span class="nav-link-icon d-inline-block">
                      <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-menu-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><line x1="4" y1="6" x2="20" y2="6"></line><line x1="4" y1="12" x2="20" y2="12"></line><line x1="4" y1="18" x2="20" y2="18"></line></svg>
                    </span>
                    <span class="nav-link-title">
                      <?=lang('NesneMarket.sayfa.nesneMarketEsya')?>
                    </span>
                  </a>
                <?php endif; ?>
                <?php if (IsAllowedViewModule('nesneMarketKategoriGorebilsin')): ?>
                  <a class="dropdown-item" href="<?=base_url('NesneMarket/Kategori')?>" >
                    <span class="nav-link-icon d-inline-block">
                      <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M4 4h6v6h-6z"></path><path d="M14 4h6v6h-6z"></path><path d="M4 14h6v6h-6z"></path><circle cx="17" cy="17" r="3"></circle></svg>
                    </span>
                    <span class="nav-link-title">
                      <?=lang('NesneMarket.sayfa.kategoriler')?>
                    </span>
                  </a>
                <?php endif; ?>
              </div>
            </li>
          <?php endif; ?>

          <?php if (
            IsAllowedViewModule('logoyuGuncelleyebilsin')
            || IsAllowedViewModule('faviconGuncelleyebilsin')
            || IsAllowedViewModule('siteAyarlariniGuncelleyebilsin')
            || IsAllowedViewModule('javascriptKodlariniGuncelleyebilsin')
            || IsAllowedViewModule('smtpAyarlariniGuncelleyebilsin')
            || IsAllowedViewModule('p2pAyarlariGuncelleyebilsin')
            || IsAllowedViewModule('ikonAyarlariGuncelleyebilsin')
            || IsAllowedViewModule('kullanicilariGorebilsin')
            || IsAllowedViewModule('efsunIsimGorebilsin')
            || IsAllowedViewModule('haritaIsimGorebilsin')
            ): ?>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="javascript:void(0)" data-bs-toggle="dropdown" role="button" aria-expanded="false" >
                <span class="nav-link-icon d-inline-block">
                  <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="4.5" cy="12" r="2.5"></circle><circle cx="20.5" cy="12" r="1.5"></circle><circle cx="13" cy="12" r="2"></circle></svg>
                </span>
                <span class="nav-link-title">
                  <?=lang('Anasayfa.sayfa.panelIslemleri')?>
                </span>
              </a>
              <div class="dropdown-menu">
                <?php if (
                  IsAllowedViewModule('efsunIsimGorebilsin')
                  || IsAllowedViewModule('haritaIsimGorebilsin')
                  ): ?>
                  <div class="dropend">
                    <a class="dropdown-item dropdown-toggle" href="#veriIslemleri" data-bs-toggle="dropdown" data-bs-auto-close="outside" role="button" aria-expanded="false" >
                      <svg xmlns="http://www.w3.org/2000/svg" class="icon me-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="14" cy="6" r="2"></circle><line x1="4" y1="6" x2="12" y2="6"></line><line x1="16" y1="6" x2="20" y2="6"></line><circle cx="8" cy="12" r="2"></circle><line x1="4" y1="12" x2="6" y2="12"></line><line x1="10" y1="12" x2="20" y2="12"></line><circle cx="17" cy="18" r="2"></circle><line x1="4" y1="18" x2="15" y2="18"></line><line x1="19" y1="18" x2="20" y2="18"></line></svg>
                      <?=lang('VeriIslemleri.sayfa.veriIslemleri')?>
                    </a>
                    <div class="dropdown-menu">
                      <?php if (IsAllowedViewModule('efsunIsimGorebilsin')): ?>
                        <a class="dropdown-item" href="<?=base_url('VeriIslemleri/ID')?>" >
                          <?=lang('VeriIslemleri.sayfa.efsunIsimleriID')?>
                        </a>
                        <a class="dropdown-item" href="<?=base_url('VeriIslemleri/Text')?>" >
                          <?=lang('VeriIslemleri.sayfa.efsunIsimleriText')?>
                        </a>
                      <?php endif; ?>
                      <?php if (IsAllowedViewModule('haritaIsimGorebilsin')): ?>
                        <a class="dropdown-item" href="<?=base_url('VeriIslemleri/Harita')?>" >
                          <?=lang('VeriIslemleri.sayfa.haritaIsimleri')?>
                        </a>
                      <?php endif; ?>
                    </div>
                  </div>
                <?php endif; ?>
                <?php if (
                  IsAllowedViewModule('logoyuGuncelleyebilsin')
                  || IsAllowedViewModule('faviconGuncelleyebilsin')
                  || IsAllowedViewModule('siteAyarlariniGuncelleyebilsin')
                  || IsAllowedViewModule('javascriptKodlariniGuncelleyebilsin')
                  || IsAllowedViewModule('smtpAyarlariniGuncelleyebilsin')
                  || IsAllowedViewModule('p2pAyarlariGuncelleyebilsin')
                  || IsAllowedViewModule('ikonAyarlariGuncelleyebilsin')
                  ): ?>
                  <div class="dropend">
                    <a class="dropdown-item dropdown-toggle" href="#ayarlar" data-bs-toggle="dropdown" data-bs-auto-close="outside" role="button" aria-expanded="false" >
                      <svg xmlns="http://www.w3.org/2000/svg" class="icon me-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M10.325 4.317c.426 -1.756 2.924 -1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543 -.94 3.31 .826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756 .426 1.756 2.924 0 3.35a1.724 1.724 0 0 0 -1.066 2.573c.94 1.543 -.826 3.31 -2.37 2.37a1.724 1.724 0 0 0 -2.572 1.065c-.426 1.756 -2.924 1.756 -3.35 0a1.724 1.724 0 0 0 -2.573 -1.066c-1.543 .94 -3.31 -.826 -2.37 -2.37a1.724 1.724 0 0 0 -1.065 -2.572c-1.756 -.426 -1.756 -2.924 0 -3.35a1.724 1.724 0 0 0 1.066 -2.573c-.94 -1.543 .826 -3.31 2.37 -2.37c1 .608 2.296 .07 2.572 -1.065z" /><circle cx="12" cy="12" r="3" /></svg>
                      <?=lang('Ayarlar.sayfa.ayarlar')?>
                    </a>
                    <div class="dropdown-menu">
                      <?php if (IsAllowedViewModule('logoyuGuncelleyebilsin')): ?>
                        <a class="dropdown-item" href="<?=base_url('Ayarlar/LogoYukle')?>" >
                          <svg xmlns="http://www.w3.org/2000/svg" class="icon me-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><line x1="15" y1="8" x2="15.01" y2="8" /><rect x="4" y="4" width="16" height="16" rx="3" /><path d="M4 15l4 -4a3 5 0 0 1 3 0l5 5" /><path d="M14 14l1 -1a3 5 0 0 1 3 0l2 2" /></svg>
                          <?=lang('Ayarlar.sayfa.logoYukle')?>
                        </a>
                      <?php endif; ?>
                      <?php if (IsAllowedViewModule('faviconGuncelleyebilsin')): ?>
                        <a class="dropdown-item" href="<?=base_url('Ayarlar/FaviconYukle')?>" >
                          <svg xmlns="http://www.w3.org/2000/svg" class="icon me-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><line x1="15" y1="8" x2="15.01" y2="8" /><rect x="4" y="4" width="16" height="16" rx="3" /><path d="M4 15l4 -4a3 5 0 0 1 3 0l5 5" /><path d="M14 14l1 -1a3 5 0 0 1 3 0l2 2" /></svg>
                          <?=lang('Ayarlar.sayfa.faviconYukle')?>
                        </a>
                      <?php endif; ?>
                      <?php if (IsAllowedViewModule('siteAyarlariniGuncelleyebilsin')): ?>
                        <a class="dropdown-item" href="<?=base_url('Ayarlar/Site')?>" >
                          <svg xmlns="http://www.w3.org/2000/svg" class="icon me-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M10.325 4.317c.426 -1.756 2.924 -1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543 -.94 3.31 .826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756 .426 1.756 2.924 0 3.35a1.724 1.724 0 0 0 -1.066 2.573c.94 1.543 -.826 3.31 -2.37 2.37a1.724 1.724 0 0 0 -2.572 1.065c-.426 1.756 -2.924 1.756 -3.35 0a1.724 1.724 0 0 0 -2.573 -1.066c-1.543 .94 -3.31 -.826 -2.37 -2.37a1.724 1.724 0 0 0 -1.065 -2.572c-1.756 -.426 -1.756 -2.924 0 -3.35a1.724 1.724 0 0 0 1.066 -2.573c-.94 -1.543 .826 -3.31 2.37 -2.37c1 .608 2.296 .07 2.572 -1.065z" /><circle cx="12" cy="12" r="3" /></svg>
                          <?=lang('Ayarlar.sayfa.siteAyarlari')?>
                        </a>
                      <?php endif; ?>
                      <?php if (IsAllowedViewModule('javascriptKodlariniGuncelleyebilsin')): ?>
                        <a class="dropdown-item" href="<?=base_url('Ayarlar/Javascript')?>" >
                          <svg xmlns="http://www.w3.org/2000/svg" class="icon me-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><polyline points="7 8 3 12 7 16" /><polyline points="17 8 21 12 17 16" /><line x1="14" y1="4" x2="10" y2="20" /></svg>
                          <?=lang('Ayarlar.sayfa.javascriptKodlari')?>
                        </a>
                      <?php endif; ?>
                      <?php if (IsAllowedViewModule('smtpAyarlariniGuncelleyebilsin')): ?>
                        <a class="dropdown-item" href="<?=base_url('Ayarlar/SMTP')?>" >
                          <svg xmlns="http://www.w3.org/2000/svg" class="icon me-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><rect x="3" y="5" width="18" height="14" rx="2" /><polyline points="3 7 12 13 21 7" /></svg>
                          <?=lang('Ayarlar.sayfa.smtpAyarlari')?>
                        </a>
                      <?php endif; ?>
                      <?php if (IsAllowedViewModule('p2pAyarlariGuncelleyebilsin')): ?>
                        <a class="dropdown-item" href="<?=base_url('Ayarlar/P2P')?>" >
                          <svg xmlns="http://www.w3.org/2000/svg" class="icon me-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M7 12l5 5l-1.5 1.5a3.536 3.536 0 1 1 -5 -5l1.5 -1.5z"></path><path d="M17 12l-5 -5l1.5 -1.5a3.536 3.536 0 1 1 5 5l-1.5 1.5z"></path><path d="M3 21l2.5 -2.5"></path><path d="M18.5 5.5l2.5 -2.5"></path><path d="M10 11l-2 2"></path><path d="M13 14l-2 2"></path></svg>
                          <?=lang('Ayarlar.sayfa.p2pAyarlari')?>
                        </a>
                      <?php endif; ?>
                      <?php if (IsAllowedViewModule('ikonAyarlariGuncelleyebilsin')): ?>
                        <a class="dropdown-item" href="<?=base_url('Ayarlar/Ikon')?>" >
                          <svg xmlns="http://www.w3.org/2000/svg" class="icon me-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><line x1="15" y1="8" x2="15.01" y2="8"></line><rect x="4" y="4" width="16" height="16" rx="3"></rect><path d="M4 15l4 -4a3 5 0 0 1 3 0l5 5"></path><path d="M14 14l1 -1a3 5 0 0 1 3 0l2 2"></path></svg>
                          <?=lang('Ayarlar.sayfa.ikonAyarlari')?>
                        </a>
                      <?php endif; ?>
                    </div>
                  </div>
                <?php endif; ?>
                <?php if (IsAllowedViewModule('kullanicilariGorebilsin')): ?>
                  <a class="dropdown-item" href="<?=base_url('Kullanicilar/Index')?>">
                    <span class="nav-link-icon d-inline-block">
                      <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><circle cx="9" cy="7" r="4" /><path d="M3 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2" /><path d="M16 3.13a4 4 0 0 1 0 7.75" /><path d="M21 21v-2a4 4 0 0 0 -3 -3.85" /></svg>
                    </span>
                    <span class="nav-link-title">
                      <?=lang('Kullanicilar.sayfa.kullanicilar')?>
                    </span>
                  </a>
                <?php endif; ?>
              </div>
            </li>
          <?php endif; ?>
        </ul>
      </div>
    </div>
  </div>
</div>
<div class="content">
