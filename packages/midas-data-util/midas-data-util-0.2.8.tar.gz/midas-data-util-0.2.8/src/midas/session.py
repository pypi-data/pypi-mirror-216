from copy import deepcopy
from datetime import datetime
from typing import Any, TypedDict
from .playfab import get_playfab_str_from_datetime
from .event import Event

class SessionDumpData(TypedDict):
	session_id: str
	user_id: str
	is_studio: bool
	timestamp: str
	version_text: str
	is_singular_version: bool
	duration: float
	revenue: int
	index: int

class Session: 
	session_id: str
	user_id: str
	is_studio: bool
	events: list[Event]
	timestamp: datetime
	version_text: str
	is_singular_version: bool
	duration: float
	revenue: int
	index: int

	def __init__(
		self, 
		events: list[Event]
	):
		# sort list
		events = sorted(events, key=lambda event: event.timestamp)

		# get event bookends
		first_event = events[0]
		last_event = events[len(events)-1]
	
		self.session_id = first_event.session_id
		self.user_id = first_event.user_id
		self.events = events
		self.is_studio = first_event.is_studio
		self.timestamp = first_event.timestamp
		self.version_text = first_event.version_text
		self.is_singular_version = True
		
		for event in events:
			if event.version_text != self.version_text:
				self.is_singular_version = False
				break

		# get duration
		self.duration = (last_event.timestamp-first_event.timestamp).total_seconds()
		self.revenue = 0
		for event in events:
			self.revenue += event.revenue

		self.index = -1
	
	def __lt__(self, other):
		t1 = self.timestamp
		t2 = other.timestamp
		return t1 < t2

	def dump(self) -> SessionDumpData:
		return {
			"session_id": self.session_id,
			"user_id": self.user_id,
			"is_studio": self.is_studio,
			"timestamp": get_playfab_str_from_datetime(self.timestamp),
			"version_text": self.version_text,
			"is_singular_version": self.is_singular_version,
			"duration": self.duration,
			"revenue": self.revenue,
			"index": self.index
		}

def get_survival_rate(sessions: list[Session]) -> float:
	missing_event_count = 0
	found_event_count = 0
	session_count = len(sessions)
	print("getting event survival rate for ", session_count, "sessions")
	for i, session in enumerate(sessions):
		# if i % 100 == 0:
		# 	print("[", i, "/", session_count, "] events: ", len(session.events))
		for event in session.events:
			found_event_count += 1

			if event.is_sequential == False:
				highest_prior_event = None

				for previous in session.events:

					if highest_prior_event == None and previous.index < event.index:
						highest_prior_event = previous

					elif highest_prior_event != None:
						maybe_event: Any = highest_prior_event
						certified_event: Event = maybe_event
						if certified_event.index < previous.index and previous.index < event.index:
							highest_prior_event = previous

				if highest_prior_event != None:

					also_maybe_event: Any = highest_prior_event
					also_certified_event: Event = also_maybe_event
					missing_event_count += event.index - also_certified_event.index - 1

	total_event_count = missing_event_count + found_event_count
			
	return found_event_count / max(total_event_count, 1)

def get_sessions_from_events(
	events: list[Event],
	sessions_must_include_exit_and_enter_events=True,
	exit_event_name="UserExitQuit", 
	enter_event_name="UserJoinEnter",
	) -> list[Session]:
	session_events: dict[str, list[Event]] = {}

	for event in events:
		if not event.session_id in session_events:
			session_events[event.session_id] = []
			
		session_events[event.session_id].append(event)
	
	print("session keys: ", len(list(session_events.keys())))

	# Sort session events by timestamp
	sessions: list[Session] = []
	for session_id in session_events:
		session_event_list = session_events[session_id]
		session_event_list = sorted(session_event_list, key=lambda session: session.timestamp)
		first_event = session_event_list[0]
		includes_bookend_events = False
		
		if len(session_event_list) > 1:
			last_event = session_event_list[len(session_event_list)-1]
			includes_bookend_events = first_event.name == enter_event_name and last_event.name == exit_event_name

		if len(session_event_list) > 0:
			if includes_bookend_events or sessions_must_include_exit_and_enter_events == False:
				sessions.append(Session(session_event_list))



				
	return sessions