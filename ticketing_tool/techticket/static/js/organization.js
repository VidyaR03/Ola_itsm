// radio button
$('.form-part input[type="radio"]').wrap('<div class="ns-radio-btn"><i></i></div>');
$(".ns-radio-btn").on('click', function() {
  var _this = $(this),
    block = _this.parent().parent();
  block.find('input:radio').attr('checked', false);
  block.find(".ns-radio-btn").removeClass('checkedRadio');
  _this.addClass('checkedRadio');
  _this.find('input:radio').attr('checked', true);
});

// checkbox
$('.form-part input[type="checkbox"]').wrap('<div class="ns-check-box"><i></i></div>');
$.fn.toggleCheckbox = function() {
  this.attr('checked', !this.attr('checked'));
}
$('.ns-check-box').on('click', function() {
  $(this).find(':checkbox').toggleCheckbox();
  $(this).toggleClass('checkedBox');
});