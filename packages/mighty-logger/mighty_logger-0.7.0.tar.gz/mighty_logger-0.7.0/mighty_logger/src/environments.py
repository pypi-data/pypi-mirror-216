"""
A module with a list of environment options in which the modules work
and entry types that can be passed to an entry in Progress bar.
\n
Copyright © 2023 Kalynovsky Valentin. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from mighty_logger.basic.lib_types.environment_type import EnvironmentType

class LogEnvironments:
	"""
	Environments of Logger.
	"""
	CONSOLE = EnvironmentType("CONSOLE", 0, True, False)
	PLAIN_CONSOLE = EnvironmentType("PLAIN_CONSOLE", 1, True, False)
	HTML = EnvironmentType("HTML", 2, False, True)
	MARKDOWN = EnvironmentType("MARKDOWN", 3, False, True)
	PLAIN = EnvironmentType("PLAIN", 4, False, False)
