#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ DayCounter : check.cgi - 2011/10/07
#│ Copyright (c) KentWeb
#│ http://www.kent-web.com/
#└─────────────────────────────────

# モジュール宣言
use strict;
use CGI::Carp qw(fatalsToBrowser);

require "./init.cgi";
my %cf = &init;

print <<EOM;
Content-type: text/html

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<title>Check Mode</title>
</head>
<body>
<b>Check Mode: [ $cf{version} ]</b>
<ul>
EOM

# ログファイルのパス確認
my %log = (logfile => '累計', today_dat => '本日', yes_dat => '昨日');
foreach ( keys(%log) ) {
	if (-e $cf{$_}) {
		print "<li>$log{$_}ログファイルパス : OK\n";

		if (-r $cf{$_} && -w $cf{$_}) {
			print "<li>$log{$_}ログファイルパーミッション : OK\n";
		} else {
			print "<li>$log{$_}ログファイルパーミッション : NG\n";
		}
	} else {
		print "<li>$log{$_}ログファイルパス : NG\n";
	}
}

# 画像ディレクトリ
foreach ( $cf{gifdir1}, $cf{gifdir2} ) {
	if (-d $_) {
		print "<li>画像ディレクトリパス ( $_ ) : OK\n";
	} else {
		print "<li>画像ディレクトリパス ( $_ ) : NG\n";
	}

	# 画像チェック
	foreach my $i (0 .. 9) {
		if (-e "$_/$i.gif") {
			print "<li>画像 : $_/$i.gif : OK\n";
		} else {
			print "<li>画像 : $_/$i.gif : NG\n";
		}
	}
}

eval { require $cf{gifcat_pl}; };
if ($@) {
	print "<li>gifcat.plテスト : NG\n";
} else {
	print "<li>gifcat.plテスト : OK\n";
}

eval { require Image::Magick; };
if ($@) {
	print "<li>Image::Magickテスト : NG\n";
} else {
	print "<li>Image::Magickテスト : OK\n";
}

# 著作権表示：削除改変禁止
print <<EOM;
</ul>
<p style="font-size:10px;font-family:Verdana,Helvetica,Arial;margin-top:5em;text-align:center;">
- <a href="http://www.kent-web.com/">DayCounter</a> -
</p>
</body>
</html>
EOM
exit;

