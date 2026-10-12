$(document).ready(function(){
  const url = $('body').data('url');
  var dataTable = $('#ajax-datatable').DataTable({
    "processing":true,
    "serverSide":true,
    "dom": 'tpl',
    "sPaginationType": "simple",
    "language": {
      "url":url+"/assets/js/tr.json"
    },
    "searching": false,
    "ajax":{
      url:$('#ajax-datatable').data('url'),
      data: function ( d ) {
        d.searchType  = $('[name="searchType"]').val(),
        d.searchWhere = $('[name="searchWhere"]').val(),
        d.mobSearch   = $('[name="mobSearch"]').val()
      },
      type:"POST"
    },
  });
  $(".CanavarAra").on("submit", function(e){
    dataTable.ajax.reload();
    e.preventDefault();
  });
  $(document).on('click','[data-bs-target="#duzenle"]', function(event) {
    var id = $(this).data('id');
    $.ajax({
      type: "get",
      url: url+"/Canavar/Detay/"+id,
      beforeSend: function(){
        $(".site_loading").show();
      },
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
          $('[data-bs-dismiss="modal"]').click();
        }else {
          $('.Duzenle [name="vnum"]').val(response.vnum);
          $('.Duzenle [name="locale_name"]').val(response.locale_name);
          $('.Duzenle [name="rank"]').val(response.rank);
          $('.Duzenle [name="type"]').val(response.type);
          $('.Duzenle [name="battle_type"]').val(response.battle_type);
          $('.Duzenle [name="gold_min"]').val(response.gold_min);
          $('.Duzenle [name="gold_max"]').val(response.gold_max);
          $('.Duzenle [name="exp"]').val(response.exp);
          $('.Duzenle [name="level"]').val(response.level);
          $('.Duzenle [name="drop_item"]').val(response.drop_item);
          $('.Duzenle [name="max_hp"]').val(response.max_hp);
          $('.Duzenle [name="damage_min"]').val(response.damage_min);
          $('.Duzenle [name="damage_max"]').val(response.damage_max);
          $('.Duzenle [name="st"]').val(response.st);
          $('.Duzenle [name="dx"]').val(response.dx);
          $('.Duzenle [name="ht"]').val(response.ht);
          $('.Duzenle [name="iq"]').val(response.iq);
          $('.Duzenle [name="regen_cycle"]').val(response.regen_cycle);
          $('.Duzenle [name="regen_percent"]').val(response.regen_percent);
          $('.Duzenle [name="def"]').val(response.def);
          $('.Duzenle [name="attack_speed"]').val(response.attack_speed);
          $('.Duzenle [name="move_speed"]').val(response.move_speed);
          $('.Duzenle [name="attack_range"]').val(response.attack_range);
          $('.Duzenle [name="ai_flag"]').val(response.ai_flag);
          $('.Duzenle [name="setRaceFlag"]').val(response.setRaceFlag);
          $('.Duzenle [name="setImmuneFlag"]').val(response.setImmuneFlag);
          $('.Duzenle [name="skill_level0"]').val(response.skill_level0);
          $('.Duzenle [name="skill_vnum0"]').val(response.skill_vnum0);
          $('.Duzenle [name="skill_level1"]').val(response.skill_level1);
          $('.Duzenle [name="skill_vnum1"]').val(response.skill_vnum1);
          $('.Duzenle [name="skill_level2"]').val(response.skill_level2);
          $('.Duzenle [name="skill_vnum2"]').val(response.skill_vnum2);
          $('.Duzenle [name="skill_level3"]').val(response.skill_level3);
          $('.Duzenle [name="skill_vnum3"]').val(response.skill_vnum3);
          $('.Duzenle [name="skill_level4"]').val(response.skill_level4);
          $('.Duzenle [name="skill_vnum4"]').val(response.skill_vnum4);
          $('.Duzenle [name="enchant_curse"]').val(response.enchant_curse);
          $('.Duzenle [name="enchant_slow"]').val(response.enchant_slow);
          $('.Duzenle [name="enchant_poison"]').val(response.enchant_poison);
          $('.Duzenle [name="enchant_stun"]').val(response.enchant_stun);
          $('.Duzenle [name="enchant_critical"]').val(response.enchant_critical);
          $('.Duzenle [name="enchant_penetrate"]').val(response.enchant_penetrate);
          $('.Duzenle [name="resist_sword"]').val(response.resist_sword);
          $('.Duzenle [name="resist_twohand"]').val(response.resist_twohand);
          $('.Duzenle [name="resist_dagger"]').val(response.resist_dagger);
          $('.Duzenle [name="resist_bell"]').val(response.resist_bell);
          $('.Duzenle [name="resist_fan"]').val(response.resist_fan);
          $('.Duzenle [name="resist_bow"]').val(response.resist_bow);
          $('.Duzenle [name="resist_fire"]').val(response.resist_fire);
          $('.Duzenle [name="resist_elect"]').val(response.resist_elect);
          $('.Duzenle [name="resist_magic"]').val(response.resist_magic);
          $('.Duzenle [name="resist_wind"]').val(response.resist_wind);
          $('.Duzenle [name="resist_poison"]').val(response.resist_poison);
          $('[href="#genel"]').tab('show');
        }
      },
      complete: function(){
        $(".site_loading").hide();
      },
      dataType: "json"
    });
  });
  $(".Duzenle").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Canavar/Duzenle",
      contentType: false,
      processData: false,
      data: data,
      beforeSend: function(){
        $(".site_loading").show();
      },
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
        }else {
          toastr["success"](response.success);
          dataTable.ajax.reload();
        }
      },
      complete: function(){
        $(".site_loading").hide();
      },
      dataType: "json"
    })
    .fail(function(response) {
      toastr["error"](response.responseJSON.message);
    });
    e.preventDefault();
  });
  $(".SunucuyaGonder").on("submit", function(e){
    var data = new FormData(this);
    $.ajax({
      type: "post",
      url: url+"/Canavar/SunucuyaGonder",
      contentType: false,
      processData: false,
      data: data,
      beforeSend: function(){
        $(".site_loading").show();
      },
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
        }else {
          toastr["success"](response.success);
        }
      },
      complete: function(){
        $(".site_loading").hide();
      },
      dataType: "json"
    })
    .fail(function(response) {
      toastr["error"](response.responseJSON.message);
    });
    e.preventDefault();
  });
  $(".DropEkleButton").on("click", function(e){
    var vnum      = $('[name="vnum"]').val()
    var item_vnum = $('[name="item_vnum"]').val()
    var count     = $('[name="count"]').val()
    var prob      = $('[name="prob"]').val()
    $.ajax({
      type: "post",
      url: url+"/Canavar/DropEkle",
      data: {vnum,item_vnum,count,prob},
      beforeSend: function(){
        $(".site_loading").show();
      },
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
        }else {
          toastr["success"](response.success);
          dataTableDroplar.ajax.reload();
        }
      },
      complete: function(){
        $(".site_loading").hide();
      },
      dataType: "json"
    })
    .fail(function(response) {
      toastr["error"](response.responseJSON.message);
    });
    e.preventDefault();
  });
  $(document).on('click','[data-bs-target="#dropDuzenle"]', function(event) {
    $('#dropDuzenle [name="locale_name"]').val($(this).data('locale_name'));
    $('#dropDuzenle [name="newCount"]').val($(this).data('count'));
    $('#dropDuzenle [name="newProb"]').val($(this).data('prob'));
    $('#dropDuzenle [name="drop_item_vnum"]').val($(this).data('item_vnum'));
    $('#dropDuzenle [name="drop_count"]').val($(this).data('count'));
    $('#dropDuzenle [name="drop_prob"]').val($(this).data('prob'));
    $('#dropDuzenle [name="drop_mob_vnum"]').val($(this).data('mob_vnum'));
  });
  $(".DropGuncelleButon").on("click", function(e){
    var drop_mob_vnum   = $('[name="drop_mob_vnum"]').val()
    var drop_item_vnum = $('[name="drop_item_vnum"]').val()
    var drop_count     = $('[name="drop_count"]').val()
    var drop_prob      = $('[name="drop_prob"]').val()
    var newCount       = $('[name="newCount"]').val()
    var newProb        = $('[name="newProb"]').val()
    $.ajax({
      type: "post",
      url: url+"/Canavar/DropGuncelle",
      data: {drop_mob_vnum,drop_item_vnum,drop_count,drop_prob,newCount,newProb},
      beforeSend: function(){
        $(".site_loading").show();
      },
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
        }else {
          toastr["success"](response.success);
          dataTableDroplar.ajax.reload();
          $('#dropDuzenle').modal('hide');
        }
      },
      complete: function(){
        $(".site_loading").hide();
      },
      dataType: "json"
    })
    .fail(function(response) {
      toastr["error"](response.responseJSON.message);
    });
    e.preventDefault();
  });
  var dataTableDroplar = false;
  $('[href="#drop"]').on('show.bs.tab',function(e) {
    var vnum  = $('[name="vnum"]').val()
    if (dataTableDroplar!=false) {
      dataTableDroplar.destroy();
    }
    if (vnum>0) {
      dataTableDroplar = $('#drop-datatable').DataTable({
        "processing":true,
        "serverSide":true,
        "dom": '',
        "sPaginationType": "simple",
        "language": {
          "url":url+"/assets/js/tr.json"
        },
        "searching": false,
        "ajax":{
          url: url+'/Canavar/Droplar/'+vnum,
          type:"POST"
        },
      });
    }
  });
  $(document).on('click','.dropSil',function(e) {
    var mob_vnum  = $(this).data('mob_vnum');
    var item_vnum = $(this).data('item_vnum');
    var count     = $(this).data('count');
    var prob      = $(this).data('prob');
    $.ajax({
      type: "post",
      url: url+"/Canavar/DropSil",
      data: {mob_vnum,item_vnum,count,prob},
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
        }else {
          toastr["success"](response.success);
          dataTableDroplar.ajax.reload();
        }
      },
      dataType: "json"
    });
    e.preventDefault();
  });
  $('.Esyalar').select2({
    ajax: {
      url: url+'/Esya/Esyalar',
      dataType: 'json',
      delay : 250,
      processResults: function (data) {
        return {
          results: data
        };
      },
      cache : true
    }
  });
  $(".DropLevelEkleButton").on("click", function(e){
    var level_group_id  = $('[name="level_group_id"]').val();
    var level_start     = $('[name="level_start"]').val();
    var level_end       = $('[name="level_end"]').val();
    var level_item_vnum = $('[name="level_item_vnum"]').val();
    var level_count     = $('[name="level_count"]').val();
    var level_prob      = $('[name="level_prob"]').val();
    var vnum            = $('[name="vnum"]').val();
    $.ajax({
      type: "post",
      url: url+"/Canavar/DropLevelEkle",
      data: {level_group_id,level_start,level_end,level_item_vnum,level_count,level_prob,vnum},
      beforeSend: function(){
        $(".site_loading").show();
      },
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
        }else {
          toastr["success"](response.success);
          dataTableDropLevel.ajax.reload();
        }
      },
      complete: function(){
        $(".site_loading").hide();
      },
      dataType: "json"
    })
    .fail(function(response) {
      toastr["error"](response.responseJSON.message);
    });
    e.preventDefault();
  });
  $(document).on('click','[data-bs-target="#dropLevelDuzenle"]', function(event) {
    $('#dropLevelDuzenle [name="level_start"]').val($(this).data('level_start'));
    $('#dropLevelDuzenle [name="level_end"]').val($(this).data('level_end'));
    $('#dropLevelDuzenle [name="locale_name"]').val($(this).data('locale_name'));
    $('#dropLevelDuzenle [name="levelNewCount"]').val($(this).data('count'));
    $('#dropLevelDuzenle [name="levelNewProb"]').val($(this).data('prob'));
    $('#dropLevelDuzenle [name="drop_level_item_vnum"]').val($(this).data('item_vnum'));
    $('#dropLevelDuzenle [name="drop_level_count"]').val($(this).data('count'));
    $('#dropLevelDuzenle [name="drop_level_prob"]').val($(this).data('prob'));
    $('#dropLevelDuzenle [name="drop_level_group_id"]').val($(this).data('group_id'));
  });
  $(".DropLevelGuncelleButon").on("click", function(e){
    var drop_level_item_vnum = $('[name="drop_level_item_vnum"]').val()
    var drop_level_count     = $('[name="drop_level_count"]').val()
    var drop_level_prob      = $('[name="drop_level_prob"]').val()
    var drop_level_group_id  = $('[name="drop_level_group_id"]').val()
    var levelNewCount         = $('[name="levelNewCount"]').val()
    var levelNewProb          = $('[name="levelNewProb"]').val()
    $.ajax({
      type: "post",
      url: url+"/Canavar/DropLevelGuncelle",
      data: {drop_level_item_vnum,drop_level_count,drop_level_prob,drop_level_group_id,levelNewCount,levelNewProb},
      beforeSend: function(){
        $(".site_loading").show();
      },
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
        }else {
          toastr["success"](response.success);
          dataTableDropLevel.ajax.reload();
          $('#dropLevelDuzenle').modal('hide');
        }
      },
      complete: function(){
        $(".site_loading").hide();
      },
      dataType: "json"
    })
    .fail(function(response) {
      toastr["error"](response.responseJSON.message);
    });
    e.preventDefault();
  });
  var dataTableDropLevel = false;
  $('[href="#drop_level"]').on('show.bs.tab',function(e) {
    var vnum  = $('[name="vnum"]').val()
    if (dataTableDropLevel!=false) {
      dataTableDropLevel.destroy();
    }
    if (vnum>0) {
      dataTableDropLevel = $('#drop-level-datatable').DataTable({
        "processing":true,
        "serverSide":true,
        "dom": '',
        "sPaginationType": "simple",
        "language": {
          "url":url+"/assets/js/tr.json"
        },
        "searching": false,
        "ajax":{
          url: url+'/Canavar/DropLevel/'+vnum,
          type:"POST"
        },
      });
    }
  });
  $(document).on('click','.dropLevelSil',function(e) {
    var group_id  = $(this).data('group_id');
    var item_vnum = $(this).data('item_vnum');
    var count     = $(this).data('count');
    var prob      = $(this).data('prob');
    $.ajax({
      type: "post",
      url: url+"/Canavar/DropLevelSil",
      data: {group_id,item_vnum,count,prob},
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
        }else {
          toastr["success"](response.success);
          dataTableDropLevel.ajax.reload();
        }
      },
      dataType: "json"
    });
    e.preventDefault();
  });
  $(".DropKillEkleButton").on("click", function(e){
    var kill_group_id       = $('[name="kill_group_id"]').val();
    var kill_kill_per_drop  = $('[name="kill_kill_per_drop"]').val();
    var kill_item_vnum      = $('[name="kill_item_vnum"]').val();
    var kill_count          = $('[name="kill_count"]').val();
    var kill_part_prob      = $('[name="kill_part_prob"]').val();
    var vnum                = $('[name="vnum"]').val();
    $.ajax({
      type: "post",
      url: url+"/Canavar/DropKillEkle",
      data: {kill_group_id,kill_kill_per_drop,kill_item_vnum,kill_count,kill_part_prob,vnum},
      beforeSend: function(){
        $(".site_loading").show();
      },
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
        }else {
          toastr["success"](response.success);
          dataTableDropKill.ajax.reload();
        }
      },
      complete: function(){
        $(".site_loading").hide();
      },
      dataType: "json"
    })
    .fail(function(response) {
      toastr["error"](response.responseJSON.message);
    });
    e.preventDefault();
  });
  $(document).on('click','[data-bs-target="#dropKillDuzenle"]', function(event) {
    $('#dropKillDuzenle [name="kill_per_drop"]').val($(this).data('kill_per_drop'));
    $('#dropKillDuzenle [name="locale_name"]').val($(this).data('locale_name'));
    $('#dropKillDuzenle [name="killNewCount"]').val($(this).data('count'));
    $('#dropKillDuzenle [name="killNewPartProb"]').val($(this).data('part_prob'));
    $('#dropKillDuzenle [name="drop_kill_item_vnum"]').val($(this).data('item_vnum'));
    $('#dropKillDuzenle [name="drop_kill_count"]').val($(this).data('count'));
    $('#dropKillDuzenle [name="drop_kill_part_prob"]').val($(this).data('part_prob'));
    $('#dropKillDuzenle [name="drop_kill_group_id"]').val($(this).data('group_id'));
  });
  $(".DropKillGuncelleButon").on("click", function(e){
    var drop_kill_item_vnum = $('[name="drop_kill_item_vnum"]').val()
    var drop_kill_count     = $('[name="drop_kill_count"]').val()
    var drop_kill_part_prob = $('[name="drop_kill_part_prob"]').val()
    var drop_kill_group_id  = $('[name="drop_kill_group_id"]').val()
    var killNewCount        = $('[name="killNewCount"]').val()
    var killNewPartProb     = $('[name="killNewPartProb"]').val()
    $.ajax({
      type: "post",
      url: url+"/Canavar/DropKillGuncelle",
      data: {drop_kill_item_vnum,drop_kill_count,drop_kill_part_prob,drop_kill_group_id,killNewCount,killNewPartProb},
      beforeSend: function(){
        $(".site_loading").show();
      },
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
        }else {
          toastr["success"](response.success);
          dataTableDropKill.ajax.reload();
          $('#dropKillDuzenle').modal('hide');
        }
      },
      complete: function(){
        $(".site_loading").hide();
      },
      dataType: "json"
    })
    .fail(function(response) {
      toastr["error"](response.responseJSON.message);
    });
    e.preventDefault();
  });
  var dataTableDropKill = false;
  $('[href="#drop_kill"]').on('show.bs.tab',function(e) {
    var vnum  = $('[name="vnum"]').val()
    if (dataTableDropKill!=false) {
      dataTableDropKill.destroy();
    }
    if (vnum>0) {
      dataTableDropKill = $('#drop-kill-datatable').DataTable({
        "processing":true,
        "serverSide":true,
        "dom": '',
        "sPaginationType": "simple",
        "language": {
          "url":url+"/assets/js/tr.json"
        },
        "searching": false,
        "ajax":{
          url: url+'/Canavar/DropKill/'+vnum,
          type:"POST"
        },
      });
    }
  });
  $(document).on('click','.dropKillSil',function(e) {
    var group_id  = $(this).data('group_id');
    var item_vnum = $(this).data('item_vnum');
    var count     = $(this).data('count');
    var part_prob = $(this).data('part_prob');
    $.ajax({
      type: "post",
      url: url+"/Canavar/DropKillSil",
      data: {group_id,item_vnum,count,part_prob},
      success: function(response){
        if (response.error) {
          toastr["error"](response.error);
        }else {
          toastr["success"](response.success);
          dataTableDropKill.ajax.reload();
        }
      },
      dataType: "json"
    });
    e.preventDefault();
  });
});
