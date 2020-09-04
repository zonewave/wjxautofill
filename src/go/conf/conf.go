package conf

import (
	"flag"
	"github.com/BurntSushi/toml"
)

type Server struct {
	AppName         string
	HTTPPort        int
	RunMode         string
	CopyRequestBody bool
	AutoRender      bool
	EnableDocs      bool
}

type MysqlConf struct {
	Addr         string
	User         string
	Pwd          string
	DbName       string
	SystemDbName string
}

type Config struct {
	UserName        string
	PassWord        string
	MutualId        string
	InternalSeconds int
}

var (
	confPath string
	Conf     *Config
)

func init() {
	flag.StringVar(&confPath, "conf", "./conf.toml", "config path")
}

func Init() (err error) {
	_, err = toml.DecodeFile(confPath, &Conf)
	return
}
