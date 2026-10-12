<?=view('Static/Header')?>
<div class="container-xl">
  <div class="page-header d-print-none">
    <div class="row align-items-center">
      <div class="col">
        <ol class="breadcrumb breadcrumb-alternate" aria-label="breadcrumbs">
          <li class="breadcrumb-item"><a href="<?=base_url()?>"><?=lang('Esya.sayfa.esyaYonetimi')?></a></li>
          <li class="breadcrumb-item active"><a href="<?=base_url('Esya/Ara')?>"><?=lang('Esya.sayfa.ara')?></a></li>
        </ol>
      </div>
    </div>
  </div>
  <div class="row row-cards">
    <div class="col-12">
      <div class="card">
        <div class="card-body pb-0">
          <form class="EsyaAra">
            <div class="row">
              <div class="col-lg-6">
                <div class="mb-3 d-flex align-items-center">
                  <div class="me-3"><?=lang('Genel.esya')?></div>
                  <select class="form-select Esyalar" name="vnum"></select>
                </div>
                <div class="mb-3 d-flex align-items-center">
                  <div><?=lang('Genel.adet')?></div>
                  <input type="number" class="form-control ms-3" name="countStart" value="0">
                  <input type="number" class="form-control ms-3" name="countFinish" value="200">
                </div>
                <div class="mb-3 d-flex align-items-center">
                  <div><?=lang('Genel.soketler')?></div>
                  <input type="number" class="form-control ms-3" name="socket0" value="0">
                  <input type="number" class="form-control ms-3" name="socket1" value="0">
                  <input type="number" class="form-control ms-3" name="socket2" value="0">
                  <input type="number" class="form-control ms-3" name="socket3" value="0">
                  <input type="number" class="form-control ms-3" name="socket4" value="0">
                  <input type="number" class="form-control ms-3" name="socket5" value="0">
                </div>
                <div class="mb-3 d-flex align-items-center">
                  <div><?=lang('Genel.envanter')?></div>
                  <select class="form-select ms-3" name="window">
                    <option value=""></option>
                    <option value="INVENTORY"><?=lang('Genel.INVENTORY')?></option>
                    <option value="EQUIPMENT"><?=lang('Genel.EQUIPMENT')?></option>
                    <option value="SAFEBOX"><?=lang('Genel.SAFEBOX')?></option>
                    <option value="MALL"><?=lang('Genel.MALL')?></option>
                    <option value="DRAGON_SOUL_INVENTORY"><?=lang('Genel.DRAGON_SOUL_INVENTORY')?></option>
                    <option value="BELT_INVENTORY"><?=lang('Genel.BELT_INVENTORY')?></option>
                    <option value="SWITCHBOT"><?=lang('Genel.SWITCHBOT')?></option>
                    <option value="GROUND"><?=lang('Genel.GROUND')?></option>
                  </select>
                </div>
                <div class="mb-3 d-flex align-items-center">
                  <div><?=lang('Genel.gosterim')?></div>
                  <input type="number" class="form-control ms-3" name="limit" value="100">
                </div>
              </div>
              <div class="col-lg-6">
                <?php for ($i=0; $i < 5 ; $i++) { ?>
                  <div class="mb-3 d-flex align-items-center">
                    <div class="me-3"><?=lang('Genel.efsun')?></div>
                    <select class="form-select EfsunSec" name="attrtype<?=$i?>">
                      <option value=""></option>
                      <?php foreach ($efsunlar as $key => $value): ?>
                        <option value="<?=$value->id?>"><?=$value->name?></option>
                      <?php endforeach; ?>
                    </select>
                    <input type="number" class="form-control ms-3 w-25" name="attrvalue<?=$i?>" value="0">
                    <select class="form-select ms-3 w-25" name="attrequal<?=$i?>">
                      <option value="=">=</option>
                      <option value="!=">!=</option>
                    </select>
                  </div>
                <?php } ?>
              </div>
              <div class="col-12">
                <button type="submit" class="btn btn-primary w-100 mb-2"><?=lang('Esya.sayfa.ara')?></button>
              </div>
            </div>
          </form>
          <div class="row">
            <div class="table-responsive mb-0 mt-0">
              <table class="table table-striped table-borderless border-0 text-muted pt-2" data-order='[[0,"asc"]]' id="ajax-datatable" data-url="<?=base_url('Esya/AjaxAra')?>">
                <thead>
                  <tr>
                    <th class="ps-2" data-width="1%" data-class="text-truncate max-width-300"><?=lang('Genel.karakterAdi')?></th>
                    <th class="ps-2" data-width="1%" data-class="text-left text-truncate">ID</th>
                    <th class="ps-2" data-width="1%" data-class="text-left text-truncate"><?=lang('Genel.envanter')?></th>
                    <th class="ps-2" data-width="1%" data-class="text-left text-truncate">vnum</th>
                    <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Genel.esya')?></th>
                    <th class="ps-2" data-class="text-truncate max-width-300"><?=lang('Genel.adet')?></th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td colspan="6" class="text-center"><?=lang('Genel.veriYok')?></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<?=view('Static/Footer')?>
