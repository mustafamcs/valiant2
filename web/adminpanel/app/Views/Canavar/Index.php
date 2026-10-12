<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none">
    <div class="row align-items-center">
      <div class="col">
        <ol class="breadcrumb breadcrumb-alternate" aria-label="breadcrumbs">
          <li class="breadcrumb-item"><a href="<?=base_url()?>"><?=lang('Canavar.sayfa.canavar')?></a></li>
          <li class="breadcrumb-item active"><a href="<?=base_url('Canavar/Index')?>"><?=lang('Canavar.sayfa.canavarlar')?></a></li>
        </ol>
      </div>
      <?php if (IsAllowedViewModule('canavarDuzenleyebilsin')): ?>
        <div class="col-auto d-md-flex">
          <?php if (p2pStatus==1): ?>
            <form class="SunucuyaGonder">
              <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
              <button type="submit" class="btn btn-primary me-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-server-cog" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><rect x="3" y="4" width="18" height="8" rx="3"></rect><path d="M12 20h-6a3 3 0 0 1 -3 -3v-2a3 3 0 0 1 3 -3h10.5"></path><circle cx="18.001" cy="18" r="2"></circle><path d="M18.001 14.5v1.5"></path><path d="M18.001 20v1.5"></path><path d="M21.032 16.25l-1.299 .75"></path><path d="M16.27 19l-1.3 .75"></path><path d="M14.97 16.25l1.3 .75"></path><path d="M19.733 19l1.3 .75"></path><path d="M7 8v.01"></path><path d="M7 16v.01"></path></svg>
                <?=lang('Genel.sunucuyaGonder')?>
              </button>
            </form>
          <?php endif; ?>
        </div>
      <?php endif; ?>
    </div>
  </div>
  <div class="row row-cards">
    <div class="col-12">
      <div class="card">
        <div class="card-body pb-0">
          <form class="CanavarAra">
            <div class="row">
              <div class="col-lg-5">
                <div class="mb-3 d-flex align-items-center">
                  <select class="form-select" name="searchType">
                    <option value="vnum">vnum</option>
                    <option value="locale_name" selected><?=lang('Canavar.sayfa.canavarAdi')?></option>
                    <option value="rank"><?=lang('Canavar.sayfa.rank')?></option>
                    <option value="type"><?=lang('Canavar.sayfa.type')?></option>
                    <option value="level"><?=lang('Genel.seviye')?></option>
                  </select>
                </div>
              </div>
              <div class="col-lg-1">
                <div class="mb-3 d-flex align-items-center">
                  <select class="form-select" name="searchWhere">
                    <option value="=">=</option>
                    <option value="!=">!=</option>
                    <option value="%" selected>%%</option>
                  </select>
                </div>
              </div>
              <div class="col-lg-4">
                <div class="input-icon">
                  <span class="input-icon-addon">
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="10" cy="10" r="7"></circle><line x1="21" y1="21" x2="15" y2="15"></line></svg>
                  </span>
                  <input type="text" class="form-control" autocomplete="off" name="mobSearch" placeholder="<?=lang('Genel.arama')?>" aria-label="<?=lang('Genel.arama')?>">
                </div>
              </div>
              <div class="col-lg-2">
                <button type="submit" class="btn btn-primary w-100 mb-2"><?=lang('Canavar.sayfa.ara')?></button>
              </div>
            </div>
          </form>
          <div class="row">
            <div class="table-responsive mb-0 mt-0">
              <table class="table table-striped table-borderless border-0 text-muted pt-2" data-order='[[0,"asc"]]' data-page-length='10' id="ajax-datatable" data-url="<?=base_url('Canavar/Ajax')?>">
                <thead>
                  <tr>
                    <th class="ps-2" data-width="1%" data-class="text-left align-middle text-truncate">#</th>
                    <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Canavar.sayfa.canavarAdi')?></th>
                    <th class="ps-2" data-width="1%" data-class="text-truncate align-middle max-width-300"><?=lang('Canavar.sayfa.rank')?></th>
                    <th class="ps-2" data-width="1%" data-class="text-truncate align-middle max-width-300"><?=lang('Canavar.sayfa.type')?></th>
                    <th class="ps-2" data-width="1%" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.seviye')?></th>
                    <th class="ps-2" data-width="1%" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.fiyat')?></th>
                    <th class="ps-2" data-width="1%" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.exp')?></th>
                    <?php if (IsAllowedViewModule('canavarDuzenleyebilsin')): ?>
                      <th class="ps-2" data-width="1%" data-orderable="false" data-class="text-center align-middle text-truncate"><?=lang('Genel.islemler')?></th>
                    <?php endif; ?>
                  </tr>
                </thead>
                <tbody></tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<?php if (IsAllowedViewModule('canavarDuzenleyebilsin')): ?>
  <div class="modal modal-blur fade" id="duzenle" role="dialog" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
    <div class="modal-dialog modal-xl modal-dialog-centered modal-dialog-scrollable" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title"><?=lang('Canavar.sayfa.canavarDuzenle')?></h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <form class="Duzenle overflow-auto">
          <div class="modal-body pb-3">
            <div class="card">
              <div class="card-body p-0">
                <ul class="nav nav-tabs" data-bs-toggle="tabs">
                  <li class="nav-item">
                    <a href="#genel" class="nav-link active" data-bs-toggle="tab"><?=lang('Canavar.sayfa.genel')?></a>
                  </li>
                  <li class="nav-item">
                    <a href="#beden" class="nav-link" data-bs-toggle="tab"><?=lang('Canavar.sayfa.beden')?></a>
                  </li>
                  <li class="nav-item">
                    <a href="#yetenek" class="nav-link" data-bs-toggle="tab"><?=lang('Canavar.sayfa.yetenek')?></a>
                  </li>
                  <li class="nav-item">
                    <a href="#savunma" class="nav-link" data-bs-toggle="tab"><?=lang('Canavar.sayfa.savunma')?></a>
                  </li>
                  <li class="nav-item">
                    <a href="#drop" class="nav-link" data-bs-toggle="tab"><?=lang('Canavar.sayfa.drop')?></a>
                  </li>
                  <li class="nav-item">
                    <a href="#drop_level" class="nav-link" data-bs-toggle="tab"><?=lang('Canavar.sayfa.dropLevel')?></a>
                  </li>
                  <li class="nav-item">
                    <a href="#drop_kill" class="nav-link" data-bs-toggle="tab"><?=lang('Canavar.sayfa.dropKill')?></a>
                  </li>
                </ul>
                <div class="tab-content p-3">
                  <div class="tab-pane active show" id="genel">
                    <div class="row">
                      <div class="col-lg-12 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.canavarAdi')?></div>
                        <input type="text" name="locale_name" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.rank')?></div>
                        <input type="number" name="rank" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.type')?></div>
                        <input type="number" name="type" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.battle_type')?></div>
                        <input type="number" name="battle_type" class="form-control">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.gold_min')?></div>
                        <input type="number" name="gold_min" class="form-control">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.gold_max')?></div>
                        <input type="number" name="gold_max" class="form-control">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.exp')?></div>
                        <input type="number" name="exp" class="form-control">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.level')?></div>
                        <input type="number" name="level" class="form-control">
                      </div>
                      <div class="col-lg-12 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.drop_item')?></div>
                        <input type="number" name="drop_item" class="form-control">
                      </div>
                    </div>
                  </div>
                  <div class="tab-pane" id="beden">
                    <div class="row">
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.max_hp')?></div>
                        <input type="number" name="max_hp" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.damage_min')?></div>
                        <input type="number" name="damage_min" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.damage_max')?></div>
                        <input type="number" name="damage_max" class="form-control">
                      </div>
                      <div class="col-lg-3 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.st')?></div>
                        <input type="number" name="st" class="form-control">
                      </div>
                      <div class="col-lg-3 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.dx')?></div>
                        <input type="number" name="dx" class="form-control">
                      </div>
                      <div class="col-lg-3 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.ht')?></div>
                        <input type="number" name="ht" class="form-control">
                      </div>
                      <div class="col-lg-3 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.iq')?></div>
                        <input type="number" name="iq" class="form-control">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.regen_cycle')?></div>
                        <input type="number" name="regen_cycle" class="form-control">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.regen_percent')?></div>
                        <input type="number" name="regen_percent" class="form-control">
                      </div>
                      <div class="col-lg-3 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.def')?></div>
                        <input type="number" name="def" class="form-control">
                      </div>
                      <div class="col-lg-3 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.attack_speed')?></div>
                        <input type="number" name="attack_speed" class="form-control">
                      </div>
                      <div class="col-lg-3 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.move_speed')?></div>
                        <input type="number" name="move_speed" class="form-control">
                      </div>
                      <div class="col-lg-3 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.attack_range')?></div>
                        <input type="number" name="attack_range" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.ai_flag')?></div>
                        <input type="text" name="ai_flag" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.setRaceFlag')?></div>
                        <input type="text" name="setRaceFlag" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.setImmuneFlag')?></div>
                        <input type="text" name="setImmuneFlag" class="form-control">
                      </div>
                    </div>
                  </div>
                  <div class="tab-pane" id="yetenek">
                    <div class="row">
                      <?php for ($i=0; $i < 5 ; $i++) { ?>
                        <div class="col-lg-6 mb-2">
                          <div class="form-label"><?=lang('Canavar.sayfa.skill_level').' '.$i?></div>
                          <input type="number" name="skill_level<?=$i?>" class="form-control">
                        </div>
                        <div class="col-lg-6 mb-2">
                          <div class="form-label"><?=lang('Canavar.sayfa.skill_vnum').' '.$i?></div>
                          <input type="number" name="skill_vnum<?=$i?>" class="form-control">
                        </div>
                      <?php } ?>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.enchant_curse')?></div>
                        <input type="number" name="enchant_curse" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.enchant_slow')?></div>
                        <input type="number" name="enchant_slow" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.enchant_poison')?></div>
                        <input type="number" name="enchant_poison" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.enchant_stun')?></div>
                        <input type="number" name="enchant_stun" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.enchant_critical')?></div>
                        <input type="number" name="enchant_critical" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.enchant_penetrate')?></div>
                        <input type="number" name="enchant_penetrate" class="form-control">
                      </div>
                    </div>
                  </div>
                  <div class="tab-pane" id="savunma">
                    <div class="row">
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.resist_sword')?></div>
                        <input type="number" name="resist_sword" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.resist_twohand')?></div>
                        <input type="number" name="resist_twohand" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.resist_dagger')?></div>
                        <input type="number" name="resist_dagger" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.resist_bell')?></div>
                        <input type="number" name="resist_bell" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.resist_fan')?></div>
                        <input type="number" name="resist_fan" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.resist_bow')?></div>
                        <input type="number" name="resist_bow" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.resist_fire')?></div>
                        <input type="number" name="resist_fire" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.resist_elect')?></div>
                        <input type="number" name="resist_elect" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.resist_magic')?></div>
                        <input type="number" name="resist_magic" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.resist_wind')?></div>
                        <input type="number" name="resist_wind" class="form-control">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.resist_poison')?></div>
                        <input type="number" name="resist_poison" class="form-control">
                      </div>
                    </div>
                  </div>
                  <div class="tab-pane" id="drop">
                    <div class="row">
                      <div class="col-lg-3 mb-2">
                        <div class="form-label"><?=lang('Genel.esya')?></div>
                        <select class="form-select Esyalar" name="item_vnum"></select>
                      </div>
                      <div class="col-lg-3 mb-2">
                        <div class="form-label"><?=lang('Genel.adet')?></div>
                        <input type="number" name="count" class="form-control" value="1">
                      </div>
                      <div class="col-lg-3 mb-2">
                        <div class="form-label"><?=lang('Genel.sans')?></div>
                        <input type="text" name="prob" class="form-control" value="0">
                      </div>
                      <div class="col-lg-3 mb-2">
                        <button type="button" class="btn btn-primary w-100 DropEkleButton" style="margin-top:28px;"><?=lang('Canavar.sayfa.dropEkle')?></button>
                      </div>
                    </div>
                    <hr>
                    <div class="table-responsive mb-0 mt-0">
                      <table class="table table-striped table-borderless border-0 text-muted pt-2 w-100" data-order='[[0,"asc"]]' id="drop-datatable">
                        <thead>
                          <tr>
                            <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.esya')?></th>
                            <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.adet')?></th>
                            <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.sans')?></th>
                            <th class="ps-2" data-orderable="false" data-class="text-center align-middle text-truncate"><?=lang('Genel.islemler')?></th>
                          </tr>
                        </thead>
                        <tbody></tbody>
                      </table>
                    </div>
                    <div class="modal modal-blur fade" id="dropDuzenle" role="dialog" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
                      <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable" role="document">
                        <div class="modal-content">
                          <div class="modal-header">
                            <h5 class="modal-title"><?=lang('Canavar.sayfa.dropDuzenle')?></h5>
                            <button type="button" class="btn-close" onclick="$('#dropDuzenle').modal('hide');"></button>
                          </div>
                          <div class="modal-body pb-1">
                            <div class="row">
                              <div class="col-lg-12 mb-2">
                                <div class="form-label"><?=lang('Genel.esya')?></div>
                                <input type="text" name="locale_name" class="form-control" disabled>
                              </div>
                              <div class="col-lg-6 mb-2">
                                <div class="form-label"><?=lang('Genel.adet')?></div>
                                <input type="number" name="newCount" class="form-control">
                              </div>
                              <div class="col-lg-6 mb-2">
                                <div class="form-label"><?=lang('Genel.sans')?></div>
                                <input type="text" name="newProb" class="form-control">
                              </div>
                            </div>
                            <input type="hidden" name="drop_item_vnum" value="">
                            <input type="hidden" name="drop_count" value="">
                            <input type="hidden" name="drop_prob" value="">
                            <input type="hidden" name="drop_mob_vnum" value="">
                            <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
                          </div>
                          <div class="modal-footer">
                            <div class="row w-100">
                              <div class="col-6">
                                <button type="button" class="btn w-100" onclick="$('#dropDuzenle').modal('hide');"><?=lang('Genel.iptal')?></button>
                              </div>
                              <div class="col-6">
                                <button type="submit" class="btn btn-primary w-100 DropGuncelleButon"><?=lang('Canavar.sayfa.dropDuzenle')?></button>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="tab-pane" id="drop_level">
                    <div class="row">
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.group_id')?></div>
                        <input type="number" name="level_group_id" class="form-control" value="0">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.levelBaslangic')?></div>
                        <input type="number" name="level_start" class="form-control" value="0">
                      </div>
                      <div class="col-lg-4 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.levelBitis')?></div>
                        <input type="number" name="level_end" class="form-control" value="0">
                      </div>
                      <div class="col-lg-3 mb-2">
                        <div class="form-label"><?=lang('Genel.esya')?></div>
                        <select class="form-select Esyalar" name="level_item_vnum"></select>
                      </div>
                      <div class="col-lg-3 mb-2">
                        <div class="form-label"><?=lang('Genel.adet')?></div>
                        <input type="number" name="level_count" class="form-control" value="1">
                      </div>
                      <div class="col-lg-3 mb-2">
                        <div class="form-label"><?=lang('Genel.sans')?></div>
                        <input type="text" name="level_prob" class="form-control" value="0">
                      </div>
                      <div class="col-lg-3 mb-2">
                        <button type="button" class="btn btn-primary w-100 DropLevelEkleButton" style="margin-top:28px;"><?=lang('Canavar.sayfa.dropEkle')?></button>
                      </div>
                    </div>
                    <hr>
                    <div class="table-responsive mb-0 mt-0">
                      <table class="table table-striped table-borderless border-0 text-muted pt-2 w-100" data-order='[[0,"asc"]]' id="drop-level-datatable">
                        <thead>
                          <tr>
                            <th class="ps-2" data-class="text-truncate align-middle max-width-300">#</th>
                            <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Canavar.sayfa.levelBaslangic')?></th>
                            <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Canavar.sayfa.levelBitis')?></th>
                            <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.esya')?></th>
                            <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.adet')?></th>
                            <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.sans')?></th>
                            <th class="ps-2" data-orderable="false" data-class="text-center align-middle text-truncate"><?=lang('Genel.islemler')?></th>
                          </tr>
                        </thead>
                        <tbody></tbody>
                      </table>
                    </div>
                    <div class="modal modal-blur fade" id="dropLevelDuzenle" role="dialog" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
                      <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable" role="document">
                        <div class="modal-content">
                          <div class="modal-header">
                            <h5 class="modal-title"><?=lang('Canavar.sayfa.dropDuzenle')?></h5>
                            <button type="button" class="btn-close" onclick="$('#dropLevelDuzenle').modal('hide');"></button>
                          </div>
                          <div class="modal-body pb-1">
                            <div class="row">
                              <div class="col-lg-6 mb-2">
                                <div class="form-label"><?=lang('Canavar.sayfa.levelBaslangic')?></div>
                                <input type="number" name="level_start" class="form-control" disabled>
                              </div>
                              <div class="col-lg-6 mb-2">
                                <div class="form-label"><?=lang('Canavar.sayfa.levelBitis')?></div>
                                <input type="number" name="level_end" class="form-control" disabled>
                              </div>
                              <div class="col-lg-12 mb-2">
                                <div class="form-label"><?=lang('Genel.esya')?></div>
                                <input type="text" name="locale_name" class="form-control" disabled>
                              </div>
                              <div class="col-lg-6 mb-2">
                                <div class="form-label"><?=lang('Genel.adet')?></div>
                                <input type="number" name="levelNewCount" class="form-control">
                              </div>
                              <div class="col-lg-6 mb-2">
                                <div class="form-label"><?=lang('Genel.sans')?></div>
                                <input type="text" name="levelNewProb" class="form-control">
                              </div>
                            </div>
                            <input type="hidden" name="drop_level_item_vnum" value="">
                            <input type="hidden" name="drop_level_count" value="">
                            <input type="hidden" name="drop_level_prob" value="">
                            <input type="hidden" name="drop_level_group_id" value="">
                            <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
                          </div>
                          <div class="modal-footer">
                            <div class="row w-100">
                              <div class="col-6">
                                <button type="button" class="btn w-100" onclick="$('#dropLevelDuzenle').modal('hide');"><?=lang('Genel.iptal')?></button>
                              </div>
                              <div class="col-6">
                                <button type="submit" class="btn btn-primary w-100 DropLevelGuncelleButon"><?=lang('Canavar.sayfa.dropDuzenle')?></button>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="tab-pane" id="drop_kill">
                    <div class="row">
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.group_id')?></div>
                        <input type="number" name="kill_group_id" class="form-control" value="0">
                      </div>
                      <div class="col-lg-6 mb-2">
                        <div class="form-label"><?=lang('Canavar.sayfa.killSayisi')?></div>
                        <input type="number" name="kill_kill_per_drop" class="form-control" value="0">
                      </div>
                      <div class="col-lg-3 mb-2">
                        <div class="form-label"><?=lang('Genel.esya')?></div>
                        <select class="form-select Esyalar" name="kill_item_vnum"></select>
                      </div>
                      <div class="col-lg-3 mb-2">
                        <div class="form-label"><?=lang('Genel.adet')?></div>
                        <input type="number" name="kill_count" class="form-control" value="1">
                      </div>
                      <div class="col-lg-3 mb-2">
                        <div class="form-label"><?=lang('Genel.sans')?></div>
                        <input type="text" name="kill_part_prob" class="form-control" value="0">
                      </div>
                      <div class="col-lg-3 mb-2">
                        <button type="button" class="btn btn-primary w-100 DropKillEkleButton" style="margin-top:28px;"><?=lang('Canavar.sayfa.dropEkle')?></button>
                      </div>
                    </div>
                    <hr>
                    <div class="table-responsive mb-0 mt-0">
                      <table class="table table-striped table-borderless border-0 text-muted pt-2 w-100" data-order='[[0,"asc"]]' id="drop-kill-datatable">
                        <thead>
                          <tr>
                            <th class="ps-2" data-class="text-truncate align-middle max-width-300">#</th>
                            <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Canavar.sayfa.killSayisi')?></th>
                            <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.esya')?></th>
                            <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.adet')?></th>
                            <th class="ps-2" data-class="text-truncate align-middle max-width-300"><?=lang('Genel.sans')?></th>
                            <th class="ps-2" data-orderable="false" data-class="text-center align-middle text-truncate"><?=lang('Genel.islemler')?></th>
                          </tr>
                        </thead>
                        <tbody></tbody>
                      </table>
                    </div>
                    <div class="modal modal-blur fade" id="dropKillDuzenle" role="dialog" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
                      <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable" role="document">
                        <div class="modal-content">
                          <div class="modal-header">
                            <h5 class="modal-title"><?=lang('Canavar.sayfa.dropDuzenle')?></h5>
                            <button type="button" class="btn-close" onclick="$('#dropKillDuzenle').modal('hide');"></button>
                          </div>
                          <div class="modal-body pb-1">
                            <div class="row">
                              <div class="col-lg-12 mb-2">
                                <div class="form-label"><?=lang('Canavar.sayfa.killSayisi')?></div>
                                <input type="number" name="kill_per_drop" class="form-control" disabled>
                              </div>
                              <div class="col-lg-12 mb-2">
                                <div class="form-label"><?=lang('Genel.esya')?></div>
                                <input type="text" name="locale_name" class="form-control" disabled>
                              </div>
                              <div class="col-lg-6 mb-2">
                                <div class="form-label"><?=lang('Genel.adet')?></div>
                                <input type="number" name="killNewCount" class="form-control">
                              </div>
                              <div class="col-lg-6 mb-2">
                                <div class="form-label"><?=lang('Genel.sans')?></div>
                                <input type="text" name="killNewPartProb" class="form-control">
                              </div>
                            </div>
                            <input type="hidden" name="drop_kill_item_vnum" value="">
                            <input type="hidden" name="drop_kill_count" value="">
                            <input type="hidden" name="drop_kill_part_prob" value="">
                            <input type="hidden" name="drop_kill_group_id" value="">
                            <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
                          </div>
                          <div class="modal-footer">
                            <div class="row w-100">
                              <div class="col-6">
                                <button type="button" class="btn w-100" onclick="$('#dropKillDuzenle').modal('hide');"><?=lang('Genel.iptal')?></button>
                              </div>
                              <div class="col-6">
                                <button type="submit" class="btn btn-primary w-100 DropKillGuncelleButon"><?=lang('Canavar.sayfa.dropDuzenle')?></button>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <input type="hidden" name="vnum" value="">
            <input type="hidden" name="<?=csrf_token()?>" value="<?=csrf_hash()?>">
          </div>
          <div class="modal-footer px-2">
            <div class="row w-100">
              <div class="col-6">
                <button type="button" class="btn w-100" data-bs-dismiss="modal"><?=lang('Genel.iptal')?></button>
              </div>
              <div class="col-6">
                <button type="submit" class="btn btn-primary w-100"><?=lang('Canavar.sayfa.canavarDuzenle')?></button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
<?php endif; ?>
<?=view('Static/Footer')?>
