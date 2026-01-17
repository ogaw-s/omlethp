#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ DayCounter : daycount.cgi - 2011/07/25
#│ Copyright (c) KentWeb
#│ http://www.kent-web.com/
#└─────────────────────────────────

# モジュール宣言
use strict;

# 設定ファイル取込
require './init.cgi';
my %cf = &init;

# データ受理
my $q = $ENV{QUERY_STRING};
$q =~ s/\W//g;
$q ||= 'gif';

# 未更新処理の場合
if ($q eq "yes" || ($cf{type} == 1 && $q eq "today")) {

	# データ読み込み
	my $count = &read_data;

	# 画像表示
	&load_image($count);

# 更新処理の場合
} else {

	# データ更新
	my $count = &renew_data;

	# 画像表示
	&load_image($count);
}

#-----------------------------------------------------------
#  データ更新
#-----------------------------------------------------------
sub renew_data {
	# 本日の日を取得
	$ENV{TZ} = "JST-9";
	my ($mday) = (localtime(time))[3];

	# 累計ファイル読み込み
	my $tdflg;
	open(DAT,"+< $cf{logfile}") or &error;
	eval "flock(DAT, 2);";
	my $data = <DAT>;

	# 累計ファイル分解
	my ($key, $count, $ip) = split(/\t/, $data);

	# IPチェック
	my ($ipflg, $addr);
	if ($cf{ip_check}) {
		$addr = $ENV{REMOTE_ADDR};
		if ($addr eq $ip) { $ipflg++; }
	}

	# 本日のカウント数をキーにしてカウントアップ
	if (!$ipflg) {
		# 同日
		if ($key eq $mday) {
			$tdflg = 1;

		# 日替
		} else {
			$tdflg = 2;
		}

		# カウントアップ
		$count++;

		# 累計ファイル更新
		seek(DAT, 0, 0);
		print DAT "$mday\t$count\t$addr";
		truncate(DAT, tell(DAT));
	}
	close(DAT);

	# 本日更新
	if ($tdflg == 1) {
		open(TOD,"+< $cf{today_dat}") or &error;
		eval "flock(TOD, 2);";
		my $log = <TOD>;
		seek(TOD, 0, 0);
		print TOD ++$log;
		truncate(TOD, tell(TOD));
		close(TOD);

	# 日替わりのとき（本日/昨日更新）
	} elsif ($tdflg == 2) {
		open(TOD,"+< $cf{today_dat}") or &error;
		eval "flock(TOD, 2);";
		my $log = <TOD>;
		seek(TOD, 0, 0);
		print TOD "1";
		truncate(TOD, tell(TOD));
		close(TOD);

		open(YES,"+> $cf{yes_dat}") or &error;
		eval "flock(YES, 2);";
		print YES $log;
		close(YES);
	}

	return $count;
}

#-----------------------------------------------------------
#  データ未更新
#-----------------------------------------------------------
sub read_data {
	# 少し待たせる（更新系と衝突回避）
	select(undef, undef, undef, 0.5);

	# 対象データ
	my %log = ( today => $cf{today_dat}, yes => $cf{yes_dat} );

	# 記録ファイル読み込み
	open(DAT,"$log{$q}") or &error;
	my $count = <DAT>;
	close(DAT);

	return $count;
}

#-----------------------------------------------------------
#  カウンタ画像出力
#-----------------------------------------------------------
sub load_image {
	my ($data) = @_;

	my ($digit,$dir);
	if ($q eq 'gif') {
		$digit = $cf{digit1};
		$dir = $cf{gifdir1};
	} else {
		$digit = $cf{digit2};
		$dir = $cf{gifdir2};
	}

	# 桁数調整
	while ( length($data) < $digit ) {
		$data = '0' . $data;
	}

	# Image::Magickのとき
	if ($cf{image_pm} == 1) {
		require $cf{magick_pl};
		&magick($data, $dir);
	}

	# 画像情報
	my @image;
	foreach ( split(//, $data) ) {
		push(@image,"$dir/$_.gif");
	}

	# 画像連結
	require $cf{gifcat_pl};
	print "Content-type: image/gif\n\n";
	binmode(STDOUT);
	print &gifcat::gifcat(@image);
	exit;
}

#-----------------------------------------------------------
#  エラー処理
#-----------------------------------------------------------
sub error {
	# エラー画像
	my @err = qw{
		47 49 46 38 39 61 2d 00 0f 00 80 00 00 00 00 00 ff ff ff 2c
		00 00 00 00 2d 00 0f 00 00 02 49 8c 8f a9 cb ed 0f a3 9c 34
		81 7b 03 ce 7a 23 7c 6c 00 c4 19 5c 76 8e dd ca 96 8c 9b b6
		63 89 aa ee 22 ca 3a 3d db 6a 03 f3 74 40 ac 55 ee 11 dc f9
		42 bd 22 f0 a7 34 2d 63 4e 9c 87 c7 93 fe b2 95 ae f7 0b 0e
		8b c7 de 02	00 3b
	};

	print "Content-type: image/gif\n\n";
	foreach (@err) {
		print pack('C*', hex($_));
	}
	exit;
}

