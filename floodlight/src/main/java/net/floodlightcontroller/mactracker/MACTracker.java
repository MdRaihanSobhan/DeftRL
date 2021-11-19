package net.floodlightcontroller.mactracker;

import net.floodlightcontroller.core.FloodlightContext;
import net.floodlightcontroller.core.IFloodlightProviderService;
import net.floodlightcontroller.core.IOFMessageListener;
import net.floodlightcontroller.core.IOFSwitch;
import net.floodlightcontroller.core.module.FloodlightModuleContext;
import net.floodlightcontroller.core.module.FloodlightModuleException;
import net.floodlightcontroller.core.module.IFloodlightModule;
import net.floodlightcontroller.core.module.IFloodlightService;
import net.floodlightcontroller.packet.Ethernet;
import org.openflow.protocol.OFMessage;
import org.openflow.protocol.OFType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentSkipListSet;

public class MACTracker implements IOFMessageListener, IFloodlightModule {
    protected IFloodlightProviderService floodlightProvider;
    protected Set<Integer> macAddresses;
    protected static Logger logger;

    /**
     * The name assigned to this listener
     *
     * @return
     */
    @Override
    public String getName() {
        return MACTracker.class.getSimpleName();
    }

    /**
     * Check if the module called name is a callback ordering prerequisite
     * for this module.  In other words, if this function returns true for
     * the given name, then this message listener will be called after that
     * message listener.
     *
     * @param type the message type to which this applies
     * @param name the name of the module
     * @return whether name is a prerequisite.
     */
    @Override
    public boolean isCallbackOrderingPrereq(OFType type, String name) {
        return false;
    }

    /**
     * Check if the module called name is a callback ordering post-requisite
     * for this module.  In other words, if this function returns true for
     * the given name, then this message listener will be called before that
     * message listener.
     *
     * @param type the message type to which this applies
     * @param name the name of the module
     * @return whether name is a post-requisite.
     */
    @Override
    public boolean isCallbackOrderingPostreq(OFType type, String name) {
        return false;
    }

    /**
     * This is the method Floodlight uses to call listeners with OpenFlow messages
     *
     * @param sw   the OpenFlow switch that sent this message
     * @param msg  the message
     * @param cntx a Floodlight message context object you can use to pass
     *             information between listeners
     * @return the command to continue or stop the execution
     */
    @Override
    public Command receive(IOFSwitch sw, OFMessage msg, FloodlightContext cntx) {
        logger.debug("Received");
        Ethernet eth =
                IFloodlightProviderService.bcStore.get(cntx,
                        IFloodlightProviderService.CONTEXT_PI_PAYLOAD);

        ByteBuffer bb = ByteBuffer.wrap(eth.getSourceMACAddress());
        Integer sourceMACHash = bb.getInt();
        if (!macAddresses.contains(sourceMACHash)) {
            macAddresses.add(sourceMACHash);
            logger.info("MAC Address: {} seen on switch: {}",
                    eth.getSourceMACAddress().toString(),
                    sw.getId());
        }
        return Command.CONTINUE;
    }

    /**
     * Return the list of interfaces that this module implements.
     * All interfaces must inherit IFloodlightService
     *
     * @return
     */
    @Override
    public Collection<Class<? extends IFloodlightService>> getModuleServices() {
        return null;
    }

    /**
     * Instantiate (as needed) and return objects that implement each
     * of the services exported by this module.  The map returned maps
     * the implemented service to the object.  The object could be the
     * same object or different objects for different exported services.
     *
     * @return The map from service interface class to service implementation
     */
    @Override
    public Map<Class<? extends IFloodlightService>, IFloodlightService> getServiceImpls() {
        return null;
    }

    /**
     * Get a list of Modules that this module depends on.  The module system
     * will ensure that each these dependencies is resolved before the
     * subsequent calls to init().
     *
     * @return The Collection of IFloodlightServices that this module depends
     * on.
     */
    @Override
    public Collection<Class<? extends IFloodlightService>> getModuleDependencies() {
        Collection<Class<? extends IFloodlightService>> l =
                new ArrayList<Class<? extends IFloodlightService>>();
        l.add(IFloodlightProviderService.class);
        return l;
    }

    /**
     * This is a hook for each module to do its <em>internal</em> initialization,
     * e.g., call setService(context.getService("Service"))
     * <p>
     * All module dependencies are resolved when this is called, but not every module
     * is initialized.
     *
     * @param context
     * @throws FloodlightModuleException
     */
    @Override
    public void init(FloodlightModuleContext context) throws FloodlightModuleException {
        floodlightProvider = context.getServiceImpl(IFloodlightProviderService.class);
        macAddresses = new ConcurrentSkipListSet<Integer>();
        logger = LoggerFactory.getLogger(MACTracker.class);
    }

    /**
     * This is a hook for each module to do its <em>external</em> initializations,
     * e.g., register for callbacks or query for state in other modules
     * <p>
     * It is expected that this function will not block and that modules that want
     * non-event driven CPU will spawn their own threads.
     *
     * @param context
     */
    @Override
    public void startUp(FloodlightModuleContext context) {
        floodlightProvider.addOFMessageListener(OFType.PACKET_IN, this);
    }
}