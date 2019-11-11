[About](#about) • [Installation](#installation) • [Getting started](#getting-started) • [Usage](#usage) • [License](#license)

# About

`jenkins-agent` is shell wrapper for executing Jenkins Agents. Jenkins Agent is supervised by systemd and
connected to Jenkins Master via JNLP. The user is able to specify multiple agents in simple configuration file.

## Installation

### From prebuilt package for RHEL7/CentOS7

You can find RPM packages attached to releases on [Release page](https://github.com/gongled/jenkins-agent/releases).

### From the source code

Copy shell program to system directory.

```shell
[sudo] cp SOURCES/jenkins-agent /usr/bin
[sudo] chown root:root /usr/bin/jenkins
[sudo] chmod ugo+x /usr/bin/jenkins
```

Copy systemd unit and apply changes.

```shell
[sudo] cp SOURCES/jenkins-agent@.service /etc/systemd/system/
[sudo] systemctl daemon-reload
```

Add configuration file to `/etc/jenkins-agent/jenkins-agent.conf`.

```shell
[sudo] cat << EOF > /etc/jenkins-agent/jenkins-agent.conf
[general]

  # Jenkins Slave Agent URL to jar
  jenkins_agent_url: https://ci.example.tld/jnlpJars/agent.jar
EOF
```

## Getting started

Specify Jenkins Agent profile in configuration file. `jenkins_url` and `jenkins_token` options are mandatory.

```shell
[general]

  # Jenkins Slave Agent URL to jar
  jenkins_agent_url: https://ci.example.tld/jnlpJars/agent.jar

[example]

  # Jenkins URL
  jenkins_url: https://ci.example.tld/computer/example1

  # Jenkins secret token
  jenkins_token: cfthwlbsjccmvtbfdkj39whcznkfm3lxwhvnkgfcwcmjhkzxztrjps47ftzm3fwp
```

Launch systemd unit and make sure it will be launched after reboot.

```shell
[sudo] systemctl start jenkins-agent@example.service
[sudo] systemctl enable jenkins-agent@example.service
```

Done.

## Usage

```

Usage: jenkins-agent {options}

Options

  --profile, -p profile       Jenkins Agent profile name
  --version, -v               Display version
  --help, -h                  Display this message

Examples

  jenkins-agent --profile example
  Run jenkins-agent with example profile specified in configuration file

```

## License

Released under the MIT license (see [LICENSE](LICENSE))

[![Sponsored by FunBox](https://funbox.ru/badges/sponsored_by_funbox_grayscale.svg)](https://funbox.ru)

