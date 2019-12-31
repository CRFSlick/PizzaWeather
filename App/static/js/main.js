$(document).ready(function () {

	metric = false;
	cookies = false;
	LAST_API_RESPONSE = null;

	if ($('#slider-metric').prop("checked")) {
		metric = true;
	} else {
		metric = false;
	}

	if ($('#slider-metric').prop("checked")) {
		metric = true;
	} else {
		metric = false;
	}

	$('#slider-metric').click(function () {
		if ($(this).prop("checked")) {
			metric = true;
		} else {
			metric = false;
		}

		updateData(LAST_API_RESPONSE);
	});

	$('#slider-cookies').click(function () {
		if ($(this).prop("checked")) {
			cookies = true;
		} else {
			cookies = false;
		}

		updateData(LAST_API_RESPONSE);
	});

	$(document).on('click', '.cta', function () {
		$(this).toggleClass('active');
	});

	$('.btn-toggle').click(function () {
		$(this).find('.btn').toggleClass('active');

		if ($(this).find('.btn-primary').size() > 0) {
			$(this).find('.btn').toggleClass('btn-primary');
		}
	});

	$('#homeButton').click(function (event) {
		window.location.href = "/";
	});

	$('#searchInput').keypress(function (event) {
		if (event.keyCode == 13) {
			event.preventDefault();
			$('#searchButton').click();
			return;
		}
	});

	error_event = setTimeout(function () {
		$('#errorAlert').fadeOut();
	}, 0);

	warning_event = setTimeout(function () {
		$('#warningAlert').fadeOut();
	}, 0);


	$('.page-nav').click(function (event) {
		event.preventDefault();

		$('.page-nav').each(function (event) {
			$(this).removeClass('active');
			$(this).addClass('non-active');
		});

		$('.page-container').each(function (event) {
			$(this).hide();
		});

		let element = ($(this).text()).toLowerCase().replace(/^\s+|\s+$/g, '');
		let element_div = '.page-container.' + element;
		let element_tab = '.page-nav.' + element;

		$(element_div).show();
		$(element_tab).removeClass('non-active');
		$(element_tab).addClass('active');
	});

	$('.card-nav.left').click(function (event) {
		event.preventDefault();

		$('.card-nav.left').each(function (event) {
			$(this).removeClass('active');
			$(this).addClass('non-active');
		});

		$('.card-contents.left').each(function (event) {
			$(this).hide();
		});

		let element = ($(this).text()).toLowerCase();
		let element_div = '#card-left-' + element;
		let element_tab = '#card-left-nav-tab-' + element;

		$(element_div).show();
		$(element_tab).removeClass('non-active');
		$(element_tab).addClass('active');
	});

	$('.card-nav.right').click(function (event) {
		event.preventDefault();

		$('.card-nav.right').each(function (event) {
			$(this).removeClass('active');
			$(this).addClass('non-active');
		});

		$('.card-contents.right').each(function (event) {
			$(this).hide();
		});

		let element = ($(this).text()).toLowerCase();
		let element_div = '#card-right-' + element;
		let element_tab = '#card-right-nav-tab-' + element;

		$(element_div).show();
		$(element_tab).removeClass('non-active');
		$(element_tab).addClass('active');
	});

	$('.radar-button').click(function (event) {
		event.preventDefault();

		$('.layer').each(function (event) {
			$(this).hide();
		});

		let element = ($(this).text()).toLowerCase();
		let element_class = '.layer.' + element;

		$(element_class).show();

	});

	$('#locateButton').click(function (event) {
		event.preventDefault();
		console.log('here');
		getLocation();
	});

	$('#searchButton').click(function (event) {
		event.preventDefault();
		startSearch();
	});

	$('form').on('submit', function (event) {
		event.preventDefault();
		startSearch();
	});

	$('#revealRadar').click(function () {
		if ($('#revealRadar').text() == 'More') {
			$('#radar-divider').show();
			$('#revealRadar').text('Less');
		}
		else if ($('#revealRadar').text() == 'Less') {
			$('#radar-divider').hide();
			$('#revealRadar').text('More');
		}
	});

	$('#info-temp').mouseenter(function () {
		$('#info-temp').find('#info-label-temp').fadeIn(100);
	});

	$('#info-temp').mouseleave(function () {
		$('#info-temp').find('#info-label-temp').fadeOut(100);
	});

	$('#info-cloud').mouseenter(function () {
		$('#info-cloud').find('#info-label-cloud').fadeIn(100);
	});

	$('#info-cloud').mouseleave(function () {
		$('#info-cloud').find('#info-label-cloud').fadeOut(100);
	});

	$('#info-precipitation').mouseenter(function () {
		$('#info-precipitation').find('#info-label-precipitation').fadeIn(100);
	});

	$('#info-precipitation').mouseleave(function () {
		$('#info-precipitation').find('#info-label-precipitation').fadeOut(100);
	});

	$('#info-wind').mouseenter(function () {
		$('#info-wind').find('#info-label-wind').fadeIn(100);
	});

	$('#info-wind').mouseleave(function () {
		$('#info-wind').find('#info-label-wind').fadeOut(100);
	});

	$('#info-uv').mouseenter(function () {
		$('#info-uv').find('#info-label-uv').fadeIn(100);
	});

	$('#info-uv').mouseleave(function () {
		$('#info-uv').find('#info-label-uv').fadeOut(100);
	});

	$('#info-humidity').mouseenter(function () {
		$('#info-humidity').find('#info-label-humidity').fadeIn(100);
	});

	$('#info-humidity').mouseleave(function () {
		$('#info-humidity').find('#info-label-humidity').fadeOut(100);
	});
});

function processForm() {
	if (event) {
		event.preventDefault();
	}

	hideElementsForSearch();

	if (validateData($('#searchInput').val())) {
		void(0)
	} else {
		alertError('Input Error', 'You must enter something!')
		return
	}

	startSpinner('search');

	$.ajax({
		data: {
			name: $('#searchInput').val()
		},
		type: 'GET',
		url: '/api/weather',
		timeout: 15000
	})
		.done(function (data) {
			stopSpinner('search');

			if (data.error) {
				alertError(data.error, data.error_msg);
			}
			else {
				hideAlerts();
				hideElementsForSearch();
				$('*').promise().done(function () {
					displayData(data.api_response);
					LAST_API_RESPONSE = data.api_response;
				});
				showWeatherCard();
			}
		}).fail(function (jqXHR, textStatus) {
			stopSpinner('search');
			if (textStatus === 'timeout') {
				alertError('Timeout Error', 'The server took too long to respond. Please try again!');
			}
			else {
				alertError('Internal Server Error', 'Something went wrong on our end. Please try again later.');
			}
		});
}

function validateData(data) {
	if (data.length > 0) {
		var result = parseInt(data);
		if (!isNaN(result)) {
			return 'zip';
		}
		else {
			return 'location';
		}
	} else {
		return false
	}
}

function hideElementsForSearch() {
	$('#moreCard').fadeOut();
	$('#errorAlert').fadeOut();
}

function hideDescription() {
	$('#titleCard-desc').fadeOut();
}

function showDescription() {
	$('#titleCard-desc').fadeIn();
}

function hideAlerts() {
	$('#successAlert').fadeOut();
	$('#errorAlert').fadeOut();
}

function showWeatherCard() {
	$('*').promise().done(function () {
		$('#moreCard').fadeIn();
	});
}

function startSpinner(button_name) {
	if (button_name == 'search') {
		var width = $('#searchButton').width();
		$('#searchButton').html('<i class="fas fa-spinner fa-spin h4 text-body"></i>');
		$('#searchButton').width(width);
	}

	if (button_name == 'locate') {
		$('#locateButton').html('<i class="fas fa-spinner fa-spin h4 text-body" style="color: #007bff !important;"></i>');
	}
}

function stopSpinner(button_name) {
	if (button_name == 'search') {
		$('#searchButton').html('Go!');
	}

	if (button_name == 'locate') {
		$('#locateButton').html('<i class="fas fa-location-arrow"></i>');
	}

}

function alertError(error, error_msg) {
    hideElementsForSearch();
	$('*').promise().done(function () {
		clearTimeout(error_event);
		error = `${error}: `;
		$('#errorAlert > #alert').text(error);
		$('#errorAlert > #msg').text(error_msg);
		$('#errorAlert').fadeIn();
		error_event = setTimeout(function () {
			$('#errorAlert').fadeOut();
		}, 8000);
	});
}

function alertWarning(warning) {
	$('*').promise().done(function () {
		clearTimeout(warning_event);
		$('#warningAlert').text(warning).fadeIn();
		warning_event = setTimeout(function () {
			$('#warningAlert').fadeOut();
		}, 8000);
	});
}

function upperCaseFirstLetter(string) {
	return (string).charAt(0).toUpperCase() + (string).slice(1);
}

function getLocation() {
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(processLocation, error);
	} else {
		alertError('Geolocation Error', 'This feature is not supported by your browser.');

	}
}

function processLocation(position) {

	startSpinner('search');

	$.ajax({
		data: {
			lat: position.coords.latitude,
			lon: position.coords.longitude
		},
		type: 'GET',
		url: '/api/geolocate/coordinates',
		timeout: 10000
	})
		.done(function (data) {
			stopSpinner('search');

			if (data.error) {
				alertError(data.error, data.error_msg);
			}
			else {
				hideAlerts();
				$('#searchInput').val(data.api_response.display_name);
				processForm();

			}
		}).fail(function (jqXHR, textStatus) {
			stopSpinner('search');
			if (textStatus === 'timeout') {
				alertError('Timeout Error',  'The server took too long to respond. Please try again!');
			}
			else {
				alertError('Internal Server Error', 'Something went wrong on our end. Please try again later.');
			}
		});
}

function processLocationZip(zip_code) {

	startSpinner('search');

	$.ajax({
		data: {
			zip: zip_code
		},
		type: 'GET',
		url: '/api/geolocate/zip',
		timeout: 10000
	})
		.done(function (data) {
			stopSpinner('search');

			if (data.error) {
				alertError(data.error, data.error_msg);
			}
			else {
				hideAlerts();
				$('#searchInput').val(data.api_response.display_name);
				processForm();
			}
		}).fail(function (jqXHR, textStatus) {
			stopSpinner('search');
			if (textStatus === 'timeout') {
				alertError('Timeout Error',  'The server took too long to respond. Please try again!');
			}
			else {
				alertError('Internal Server Error', 'Something went wrong on our end. Please try again later.');
			}
		});
}

function startSearch() {
	data =  $('#searchInput').val();
	data_type = validateData($('#searchInput').val());

	if (data_type) {
		if (data_type == 'location') {
			processForm();
		}
		else if (data_type == 'zip') {
			processLocationZip(data);
		}

	} else {
		alertError('Input Error', 'You must enter something!');
	}
}

function error(err) {
	hideAlerts();
	hideElementsForSearch();
	alertError('Geolocation Error', err.message);
}

function kelvinToCelcius(kelvin, round = null) {
	// T(°C) = T(K) - 273.15
	if (!round) { round = 2 };
	let celcius = (kelvin - 273.15).toFixed(round);
	return celcius
}

function kelvinToFahrenheit(kelvin, round = null) {
	// T(°F) = T(K) × 9/5 - 459.67
	if (!round) { round = 2 };
	let fahrenheit = (kelvin * 9 / 5 - 459.67).toFixed(round);
	return fahrenheit
}

function metersPerSecondToMilesPerHour(metersPerSecond, round = null) {
	// miles per hour = meters per second × 2.236936
	if (!round) { round = 2 };
	let milesPerHour = (metersPerSecond * 2.236936).toFixed(round);
	return milesPerHour;
}

function millimetersToInches(millimeters, round = null) {
	// d(″) = d(mm) / 25.4
	if (!round) { round = 2 };
	let inches = (millimeters / 25.4).toFixed(round);
	return inches.toString() + "";
}

function updateData(api_response) {
	if (metric) {
		var temp = kelvinToCelcius(api_response.temperature).toString() + " °C";
		var temp_rounded = kelvinToCelcius(api_response.temperature_rounded, 1).toString() + " °C";
		var temp_average = kelvinToCelcius(api_response.temperature_average).toString() + " °C";
		var temp_high = kelvinToCelcius(api_response.temperature_high).toString() + " °C";
		var temp_low = kelvinToCelcius(api_response.temperature_low).toString() + " °C";
		var wind_speed = api_response.wind_speed.toString() + " m/s";
		var wind_direction = api_response.wind_direction.toString() + "°";
		var cloud_cover = api_response.cloud_cover.toString() + "%";
		var precipitation = api_response.precipitation.toString() + " mm";
	}

	else if (!metric) {
		var temp = kelvinToFahrenheit(api_response.temperature).toString() + " °F";
		var temp_rounded = kelvinToFahrenheit(api_response.temperature_rounded, 1).toString() + " °F";;
		var temp_average = kelvinToFahrenheit(api_response.temperature_average).toString() + " °F";;
		var temp_high = kelvinToFahrenheit(api_response.temperature_high).toString() + " °F";;
		var temp_low = kelvinToFahrenheit(api_response.temperature_low).toString() + " °F";;
		var wind_speed = metersPerSecondToMilesPerHour(api_response.wind_speed).toString() + " mph";;
		var wind_direction = api_response.wind_direction.toString() + "°";
		var cloud_cover = api_response.cloud_cover.toString() + "%";
		var precipitation = millimetersToInches(api_response.precipitation).toString() + " in";;
	}

	$('#simple-temp').text(temp_rounded);
	$('#simple-temp-average').text(temp_average);
	$('#simple-temp-high').text(temp_high);
	$('#simple-temp-low').text(temp_low);
	$('#simple-wind-speed').text(wind_speed);
	$('#simple-wind-direction').text(wind_direction);
	$('#simple-cloud-cover').text(cloud_cover);
	$('#simple-precipitation').text(precipitation);

	$('#desc-temp').text(temp);
	$('#desc-temp-average').text(temp_average);
	$('#desc-temp-high').text(temp_high);
	$('#desc-temp-low').text(temp_low);
	$('#desc-wind-speed').text(wind_speed);
	$('#desc-wind-direction').text(wind_direction);
	$('#desc-cloud-cover').text(cloud_cover);
	$('#desc-precipitation').text(precipitation);
}

function displayData(api_response) {

	if (metric) {
		var lat = api_response.lat;
		var lon = api_response.lon;
		var city = api_response.city;
		var region = api_response.region;
		var country = api_response.country;
		var dt_date = api_response.dt_date;
		var dt_time = api_response.dt_time;
		var dt_updated = api_response.dt_updated;
		var dt_sunrise = api_response.dt_sunrise;
		var dt_sunset = api_response.dt_sunset;
		var display_name = api_response.display_name;
		var weather = upperCaseFirstLetter(api_response.weather);
		var weather_description = upperCaseFirstLetter(api_response.weather_description);
		var weather_icon_url = api_response.weather_icon_url;
		var temp = kelvinToCelcius(api_response.temperature).toString() + " °C";
		var temp_rounded = kelvinToCelcius(api_response.temperature_rounded, 1).toString() + " °C";
		var temp_average = kelvinToCelcius(api_response.temperature_average).toString() + " °C";
		var temp_high = kelvinToCelcius(api_response.temperature_high).toString() + " °C";
		var temp_low = kelvinToCelcius(api_response.temperature_low).toString() + " °C";
		var wind_speed = api_response.wind_speed.toString() + " m/s";
		var wind_direction = api_response.wind_direction.toString() + "°";
		var cloud_cover = api_response.cloud_cover.toString() + "%";
		var precipitation = api_response.precipitation.toString() + " mm";
		var humidity = api_response.humidity;
		var uv_index = api_response.uv_index;
		var radar_base = api_response.radar_base;
		var radar_precipitation = api_response.radar_precipitation;
		var radar_temperature = api_response.radar_temperature;
		var radar_pressure = api_response.radar_pressure;
		var radar_clouds = api_response.radar_clouds;
		var radar_wind = api_response.radar_wind;
	}

	else if (!metric) {
		var lat = api_response.lat;
		var lon = api_response.lon;
		var city = api_response.city;
		var region = api_response.region;
		var country = api_response.country;
		var dt_date = api_response.dt_date;
		var dt_time = api_response.dt_time;
		var dt_updated = api_response.dt_updated;
		var dt_sunrise = api_response.dt_sunrise;
		var dt_sunset = api_response.dt_sunset;
		var display_name = api_response.display_name;
		var weather = upperCaseFirstLetter(api_response.weather);
		var weather_description = upperCaseFirstLetter(api_response.weather_description);
		var weather_icon_url = api_response.weather_icon_url;
		var temp = kelvinToFahrenheit(api_response.temperature).toString() + " °F";
		var temp_rounded = kelvinToFahrenheit(api_response.temperature_rounded, 1).toString() + " °F";;
		var temp_average = kelvinToFahrenheit(api_response.temperature_average).toString() + " °F";;
		var temp_high = kelvinToFahrenheit(api_response.temperature_high).toString() + " °F";;
		var temp_low = kelvinToFahrenheit(api_response.temperature_low).toString() + " °F";;
		var wind_speed = metersPerSecondToMilesPerHour(api_response.wind_speed).toString() + " mph";;
		var wind_direction = api_response.wind_direction.toString() + "°";
		var cloud_cover = api_response.cloud_cover.toString() + "%";
		var precipitation = millimetersToInches(api_response.precipitation);
		var humidity = api_response.humidity;
		var uv_index = api_response.uv_index;
		var radar_base = api_response.radar_base;
		var radar_precipitation = api_response.radar_precipitation;
		var radar_temperature = api_response.radar_temperature;
		var radar_pressure = api_response.radar_pressure;
		var radar_clouds = api_response.radar_clouds;
		var radar_wind = api_response.radar_wind;
	}

	$('#simple-location').text(display_name);
	$('#simple-weather').text(weather);
	$('#simple-weather-description').text(weather_description);
	$('#simple-weather-icon').attr('src', weather_icon_url);
	$('#simple-temp').text(temp_rounded);
	$('#simple-temp-average').text(temp_average);
	$('#simple-temp-high').text(temp_high);
	$('#simple-temp-low').text(temp_low);
	$('#simple-wind-speed').text(wind_speed);
	$('#simple-wind-direction').text(wind_direction);
	$('#simple-cloud-cover').text(cloud_cover);
	$('#simple-precipitation').text(precipitation);
	$('#simple-humidity').text(humidity);
	$('#simple-uv-index').text(uv_index);

	$('#desc-weather').text(weather);
	$('#desc-weather-description').text(weather_description);
	$('#desc-dt-date').text(dt_date);
	$('#desc-dt-time').text(dt_time);
	$('#desc-dt-updated').text(dt_updated);
	$('#desc-dt-sunrise').text(dt_sunrise);
	$('#desc-dt-sunset').text(dt_sunset);
	$('#desc-temp').text(temp);
	$('#desc-temp-average').text(temp_average);
	$('#desc-temp-high').text(temp_high);
	$('#desc-temp-low').text(temp_low);
	$('#desc-wind-speed').text(wind_speed);
	$('#desc-wind-direction').text(wind_direction);
	$('#desc-cloud-cover').text(cloud_cover);
	$('#desc-precipitation').text(precipitation);
	$('#desc-humidity').text(humidity);
	$('#desc-uv-index').text(uv_index);

	$('#radar-lat').text(lat);
	$('#radar-lon').text(lon);
	$('#radar-city').text(city);
	$('#radar-region').text(region);
	$('#radar-country').text(country);


	$('.base.base').attr('src', 'none');
	$('.base.base').attr("src", "data:image/jpeg;base64," + radar_base);
	$('.layer.precipitation').attr("src", "data:image/jpeg;base64," + radar_precipitation);
	$('.layer.temperature').attr("src", "data:image/jpeg;base64," + radar_temperature);
	$('.layer.pressure').attr("src", "data:image/jpeg;base64," + radar_pressure);
	$('.layer.clouds').attr("src", "data:image/jpeg;base64," + radar_clouds);
	$('.layer.wind').attr("src", "data:image/jpeg;base64," + radar_wind);
}