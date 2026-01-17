#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ DayCounter : conv.cgi - 2011/10/07
#│ Copyright (c) KentWeb
#│ http://www.kent-web.com/
#└─────────────────────────────────
# [ Ver.2 から Ver.3 へログを変換するためのプログラムです ]
# [ ログ変換後は、必ず削除してください。                  ]
#
# [ 使い方 ]
#   1. 「dataディレクトリ」のパーミッションを777に設定
#   2. Ver.2で使用していた「daycount.dat」を「dataディレクトリ」に置く。
#   3. 「dataディレクトリ」の中に「today.dat」「yes.dat」を置き、共にパーミッションを666にする。
#   4. 「conv.cgi」にアクセスし、「変換完了!」の文字列が表示されたら成功。
#   5. 「conv.cgi」を削除する。

# モジュール宣言
use strict;
use CGI::Carp qw(fatalsToBrowser);

require "./init.cgi";
my %cf = &init;

# 旧データ
my $oldfile = "./data/daycount.dat";

open(IN,"$oldfile") || die;
my $data = <IN>;
close(IN);

my ($key, $yes, $tod, $count, $ip) = split(/<>/, $data);

open(DAT,"+> $cf{logfile}") || die;
print DAT "$key\t$count\t$ip";
close(DAT);

open(DAT,"+> $cf{today_dat}") || die;
print DAT $tod;
close(DAT);

open(DAT,"+> $cf{yes_dat}") || die;
print DAT $yes;
close(DAT);

chmod( 0666, $cf{logfile}, $cf{today_dat}, $cf{yes_dat} );

print <<EOM;
Content-type: text/html

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<title>変換プログラム</title>
</head>
<body>
変換完了!
</body>
</html>
EOM

