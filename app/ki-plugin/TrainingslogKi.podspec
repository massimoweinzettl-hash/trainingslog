Pod::Spec.new do |s|
  s.name = 'TrainingslogKi'
  s.version = '1.0.0'
  s.summary = 'Lokale KI (Apple Foundation Models) für den Trainingslog'
  s.license = { :type => 'Proprietary' }
  s.homepage = 'https://github.com/massimoweinzettl-hash/trainingslog'
  s.author = 'Trainingslog'
  s.source = { :git => 'https://github.com/massimoweinzettl-hash/trainingslog.git', :tag => s.version.to_s }
  s.source_files = 'ios/Sources/**/*.swift'
  s.ios.deployment_target = '15.0'
  s.dependency 'Capacitor'
  s.swift_version = '5.9'
  s.weak_frameworks = 'FoundationModels'
end
