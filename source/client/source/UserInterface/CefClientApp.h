#ifndef __CEF3_ClientHandler__
#define __CEF3_ClientHandler__

#include "../../external/include/cef/cef_app.h"
#include "../../external/include/cef/cef_client.h"

class ClientApp : public CefApp, public CefRenderProcessHandler {
public:
	ClientApp();

	CefRefPtr<CefRenderProcessHandler> GetRenderProcessHandler() OVERRIDE
	{
		return this;
	}

	void OnWebKitInitialized() OVERRIDE;

	IMPLEMENT_REFCOUNTING(ClientApp);
};

#endif /* defined(__CEF3_ClientHandler__) */
